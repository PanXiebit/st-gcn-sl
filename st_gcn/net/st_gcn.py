import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
import math
from net import Unit2D, conv_init, import_class
from unit_gcn import unit_gcn

default_backbone = [(64, 64, 1), (64, 64, 1), (64, 64, 1), (64, 128,
                                                            2), (128, 128, 1),
                    (128, 128, 1), (128, 256, 2), (256, 256, 1), (256, 256, 1)]


class Model(nn.Module):
    def __init__(self,
                 channel,
                 num_class,
                 window_size,
                 num_point,
                 num_person=1,
                 graph=None,
                 graph_args=dict(),
                 backbone_config=None,
                 multiscale=False,
                 use_data_bn=False,
                 use_local_bn=False,
                 temporal_kernel_size=9,
                 mask_learning=False):
        super(Model, self).__init__()

        if graph is None:
            raise ValueError()
        else:
            Graph = import_class(graph)
            self.graph = Graph(**graph_args)
            self.A = torch.from_numpy(self.graph.A).float().cuda(0)

        self.num_class = num_class
        self.use_data_bn = use_data_bn
        self.multiscale = multiscale

        # Different bodies share batchNorma parameters or not
        self.M_dim_bn = True 

        if self.M_dim_bn:
            self.data_bn = nn.BatchNorm1d(channel * num_point * num_person)
        else:
            self.data_bn = nn.BatchNorm1d(channel * num_point)

        kwargs = dict(
            A=self.A,
            mask_learning=mask_learning,
            use_local_bn=use_local_bn,
            kernel_size=temporal_kernel_size)

        if self.multiscale:
            unit = TCN_GCN_unit_multiscale
        else:
            unit = TCN_GCN_unit

        # backbone
        if backbone_config is None:
            backbone_config = default_backbone
        self.backbone = nn.ModuleList([
            unit(in_c, out_c, stride=stride, **kwargs)
            for in_c, out_c, stride in backbone_config
        ])
        backbone_in_c = backbone_config[0][0]
        backbone_out_c = backbone_config[-1][1]
        backbone_out_t = window_size
        backbone = []
        for in_c, out_c, stride in backbone_config:
            backbone.append(unit(in_c, out_c, stride=stride, **kwargs))
            if backbone_out_t % stride == 0:
                backbone_out_t = backbone_out_t // stride
            else:
                backbone_out_t = backbone_out_t // stride + 1
        self.backbone = nn.ModuleList(backbone)

        # head
        self.gcn0 = unit_gcn(
            channel,
            backbone_in_c,
            self.A,
            mask_learning=mask_learning,
            use_local_bn=use_local_bn)
        self.tcn0 = Unit2D(backbone_in_c, backbone_in_c, kernel_size=9)

        # tail
        self.person_bn = nn.BatchNorm1d(backbone_out_c)
        self.gap_size = backbone_out_t
        #self.fcn = nn.Conv1d(
        #    backbone_out_c, num_class, kernel_size=self.gap_size)
        self.fcn = nn.Conv1d(backbone_out_c, num_class, kernel_size=1)
        conv_init(self.fcn)

    def forward(self, x):
        N, C, T, V, M = x.size()  

        # data bn
        if self.use_data_bn:
            if self.M_dim_bn:
                x = x.permute(0, 4, 3, 1, 2).contiguous().view(N, M * V * C, T)
            else:
                x = x.permute(0, 4, 3, 1, 2).contiguous().view(N * M, V * C, T)

            x = self.data_bn(x)
            # to (N*M, C, T, V)
            x = x.view(N, M, V, C, T).permute(0, 1, 3, 4, 2).contiguous().view(
                N * M, C, T, V)
        else:
            # from (N, C, T, V, M) to (N*M, C, T, V)
            x = x.permute(0, 4, 1, 2, 3).contiguous().view(N * M, C, T, V)

        # model
        x = self.gcn0(x)
        x = self.tcn0(x)
        for  m in self.backbone:
            x = m(x)

        # V pooling
        x = F.avg_pool2d(x, kernel_size=(1, V))

        # M pooling
        x = x.view(N, M, x.size(1), x.size(2))
        x = x.mean(dim=1)

        # T pooling
        x = F.avg_pool1d(x, kernel_size=x.size()[2])
        # x = F.avg_pool1d(x, kernel_size=self.gap_size)

        # C fcn
        x = self.fcn(x)
        x = F.avg_pool1d(x, x.size()[2:])
        x = x.view(N, self.num_class)

        return x

class TCN_GCN_unit(nn.Module):
    def __init__(self,
                 in_channel,
                 out_channel,
                 A,
                 kernel_size=9,
                 stride=1,
                 dropout=0.5,
                 use_local_bn=False,
                 mask_learning=False):
        super(TCN_GCN_unit, self).__init__()
        half_out_channel = out_channel / 2
        self.A = A
        self.V = A.size()[-1]
        self.C = in_channel

        self.gcn1 = unit_gcn(
            in_channel,
            out_channel,
            A,
            use_local_bn=use_local_bn,
            mask_learning=mask_learning)
        self.tcn1 = Unit2D(
            out_channel,
            out_channel,
            kernel_size=kernel_size,
            dropout=dropout,
            stride=stride)
        if (in_channel != out_channel) or (stride != 1):
            self.down1 = Unit2D(
                in_channel, out_channel, kernel_size=1, stride=stride)
        else:
            self.down1 = None

    def forward(self, x):
        # N, C, T, V = x.size()
        x = self.tcn1(self.gcn1(x)) + (x if (self.down1 is None) else
                                       self.down1(x))
        return x

class TCN_GCN_unit_multiscale(nn.Module):
    def __init__(self,
                 in_channels,
                 out_channels,
                 A,
                 kernel_size=9,
                 stride=1,
                 **kwargs):
        super(TCN_GCN_unit_multiscale, self).__init__()
        self.unit_1 = TCN_GCN_unit(in_channels, out_channels/2, A, kernel_size=kernel_size, stride=stride, **kwargs)
        self.unit_2 = TCN_GCN_unit(in_channels, out_channels-out_channels/2, A, kernel_size=kernel_size*2-1, stride=stride, **kwargs)

    def forward(self, x):
        return torch.cat((self.unit_1(x), self.unit_2(x)), dim=1)
