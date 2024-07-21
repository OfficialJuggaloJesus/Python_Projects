import torch
import torch.optim as optim
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt

# Load and preprocess images
def load_image(img_path, max_size=400, shape=None):
    image = Image.open(img_path)
    if max(image.size) > max_size:
        size = max_size
    else:
        size = max(image.size)
    if shape:
        size = shape
    image = transforms.Resize(size)(image)
    image = transforms.ToTensor()(image).unsqueeze(0)
    return image

def imshow(tensor, title=None):
    image = tensor.cpu().clone()
    image = image.squeeze(0)
    image = transforms.ToPILImage()(image)
    plt.imshow(image)
    if title:
        plt.title(title)
    plt.pause(0.001)

# Define loss functions
def content_loss(target, content):
    return torch.mean((target - content) ** 2)

def gram_matrix(tensor):
    batch_size, channels, height, width = tensor.size()
    features = tensor.view(batch_size * channels, height * width)
    gram = torch.mm(features, features.t())
    return gram

def style_loss(target, style):
    target_gram = gram_matrix(target)
    style_gram = gram_matrix(style)
    return torch.mean((target_gram - style_gram) ** 2)

# Load pre-trained VGG19 model
class VGG19(nn.Module):
    def __init__(self, model):
        super(VGG19, self).__init__()
        self.model = model
    
    def forward(self, x):
        features = []
        for name, layer in self.model._modules.items():
            x = layer(x)
            if name in {'0', '5', '10', '19', '28'}:
                features.append(x)
        return features

vgg = models.vgg19(pretrained=True).features.eval()
vgg = VGG19(vgg)

# Define the model and optimization
def get_model_and_optimizer(generated_img):
    optimizer = optim.LBFGS([generated_img.requires_grad_()])
    return optimizer

def run_style_transfer(content_img, style_img, generated_img, num_steps=300):
    optimizer = get_model_and_optimizer(generated_img)
    style_weight = 1e6
    content_weight = 1e0
    
    content_features = vgg(content_img)[2]
    style_features = vgg(style_img)[2]

    for step in range(num_steps):
        def closure():
            generated_img.data.clamp_(0, 1)
            optimizer.zero_grad()
            generated_features = vgg(generated_img)
            
            c_loss = content_loss(generated_features[2], content_features)
            s_loss = style_loss(generated_features[2], style_features)
            
            loss = content_weight * c_loss + style_weight * s_loss
            loss.backward()
            return loss
        
        optimizer.step(closure)
        if step % 50 == 0:
            print(f"Step {step}, Loss: {closure().item()}")
            imshow(generated_img, title=f"Step {step}")

    generated_img.data.clamp_(0, 1)
    imshow(generated_img, title="Final Result")

# Paths to images
content_img_path = 'card_back.png'
style_img_path = 'card_back.png'

# Load images
content_img = load_image(content_img_path, shape=(400, 400))
style_img = load_image(style_img_path, shape=(400, 400))

# Initialize generated image with content image
generated_img = content_img.clone()

# Run style transfer
run_style_transfer(content_img, style_img, generated_img)
