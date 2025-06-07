import torch
# t = torch.tensor([[1,2,3],[1,2,3]])
# print(t)
print(torch.cuda.device(0),torch.cuda.get_device_name(0))