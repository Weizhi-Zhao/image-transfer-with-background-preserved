import os
import argparse
from PIL import Image
import numpy as np
import torch
from torchvision.transforms.functional import to_tensor, to_pil_image
from model import Generator
import numpy as np
import torch
import matplotlib.pyplot as plt
import cv2
from segment_anything import sam_model_registry, SamPredictor

torch.backends.cudnn.enabled = False
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True

IMAGE_PATH = "samples/inputs/shield.jpg"
sam_checkpoint = "sam_vit_l_0b3195.pth"
model_type = "vit_l"


def load_image(image_path, x32=False):
    img = Image.open(image_path).convert("RGB")

    if x32:
        def to_32s(x):
            return 256 if x < 256 else x - x % 32
        w, h = img.size
        img = img.resize((to_32s(w), to_32s(h)))

    return img


def test(args, image):
    device = args.device
    
    net = Generator()
    net.load_state_dict(torch.load(args.checkpoint, map_location="cpu"))
    net.to(device).eval()
    print(f"model loaded: {args.checkpoint}")
    
    os.makedirs(args.output_dir, exist_ok=True)

    with torch.no_grad():
        image = to_tensor(image).unsqueeze(0) * 2 - 1
        out = net(image.to(device), args.upsample_align).cpu()
        out = out.squeeze(0).clip(-1, 1) * 0.5 + 0.5
        out = to_pil_image(out)

    out.save(os.path.join(args.output_dir, IMAGE_PATH.split("/")[-1]))
    return out

def show_mask(mask, ax, random_color=False):
    if random_color:
        color = np.concatenate([np.random.random(3), np.array([0.6])], axis=0)
    else:
        color = np.array([30/255, 144/255, 255/255, 0.6])
    h, w = mask.shape[-2:]
    mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
    ax.imshow(mask_image)
    
def show_points(coords, labels, ax, marker_size=375):
    pos_points = coords[labels==1]
    neg_points = coords[labels==0]
    ax.scatter(pos_points[:, 0], pos_points[:, 1], color='green', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)
    ax.scatter(neg_points[:, 0], neg_points[:, 1], color='red', marker='*', s=marker_size, edgecolor='white', linewidth=1.25)   
    
def show_box(box, ax):
    x0, y0 = box[0], box[1]
    w, h = box[2] - box[0], box[3] - box[1]
    ax.add_patch(plt.Rectangle((x0, y0), w, h, edgecolor='green', facecolor=(0,0,0,0), lw=2))   

image = cv2.imread(IMAGE_PATH)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.figure(figsize=(10,10))
plt.imshow(image)
plt.axis('on')
plt.show()

device = "cpu"

sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
sam.to(device=device)

predictor = SamPredictor(sam)

predictor.set_image(image)

# input_point = np.array([[1260, 600]])
# input_point = np.array([[960, 600]])
input_point = np.array([[660, 600]])
input_label = np.array([1])

masks, scores, logits = predictor.predict(
    point_coords=input_point,
    point_labels=input_label,
    multimask_output=True,
)

mask = masks[2]
plt.figure(figsize=(10,10))
plt.imshow(image)
show_mask(mask, plt.gca())
show_points(input_point, input_label, plt.gca())
plt.axis('off')
plt.show()

mask = mask.astype(np.uint8)
mask[mask==1] = 255

import cv2

img = cv2.imread(IMAGE_PATH)

img1gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

mask_inv = cv2.bitwise_not(mask)

img_fg = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow('sam result', img_fg)

cv2.waitKey(0)

cv2.destroyAllWindows()

parser = argparse.ArgumentParser()
parser.add_argument(
    '--checkpoint',
    type=str,
    default='./weights/celeba_distill.pt',
)
parser.add_argument(
    '--input_dir', 
    type=str, 
    default='./samples/inputs',
)
parser.add_argument(
    '--output_dir', 
    type=str, 
    default='./samples/results',
)
parser.add_argument(
    '--device',
    type=str,
    default='cpu',
)
parser.add_argument(
    '--upsample_align',
    type=bool,
    default=False,
    help="Align corners in decoder upsampling layers"
)
parser.add_argument(
    '--x32',
    action="store_true",
    help="Resize images to multiple of 32"
)
args = parser.parse_args()

img_fga = test(args, image)
img_fga = cv2.cvtColor(np.asarray(img_fga),cv2.COLOR_RGB2BGR) 
img_fga = cv2.bitwise_and(img_fga, img_fga, mask=mask)

img_bg = cv2.bitwise_and(img, img, mask=mask_inv)

res = cv2.add(img_fga, img_bg)

cv2.imshow('result', res)

cv2.waitKey(0)

cv2.destroyAllWindows()