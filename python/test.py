from __future__ import print_function
import torch

x = torch.empty(5, 3)

y = torch.rand(5, 3)
print(x)
print(y)
print(x + y)

print(y[:, 1])

x = torch.randn(4, 4)
y = x.view(16)
z = x.view(-1, 8)  # the size -1 is inferred from other dimensions
print(x.size(), y.size(), z.size())

print(x)
print(y)