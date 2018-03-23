import os

import numpy as np
import scipy.misc as misc

base_dir_train = "../ISPRS_semantic_labeling_Vaihingen/train_5channels"
base_dir_tiny_train = "../ISPRS_semantic_labeling_Vaihingen/tiny_train_5channels"
base_dir_validate = "../ISPRS_semantic_labeling_Vaihingen/validate_5channels"
base_dir_annotations = "../ISPRS_semantic_labeling_Vaihingen/annotations"
base_dir_top = "../ISPRS_semantic_labeling_Vaihingen/top"
base_dir_ndsm = "../ISPRS_semantic_labeling_Vaihingen/ndsm"
base_dir_dsm = "../ISPRS_semantic_labeling_Vaihingen/dsm"
base_dir_tiny_train_gt = "../ISPRS_semantic_labeling_Vaihingen/tiny_train_gt_5channels"
base_dir_train_validate_gt = "../ISPRS_semantic_labeling_Vaihingen/train_validate_gt_5channels"
image_size = 224
num_cropping_per_image = 3333
#validate_image = ["top_mosaic_09cm_area7.png","top_mosaic_09cm_area17.png","top_mosaic_09cm_area23.png","top_mosaic_09cm_area37.png"]
validate_image=[]

def create_training_dataset():
    for filename in os.listdir(base_dir_annotations):
        if filename in validate_image:
            continue
        top_image = misc.imread(os.path.join(base_dir_top,os.path.splitext(filename)[0]+".tif"))
        annotation_image = misc.imread(os.path.join(base_dir_annotations, filename))
        dsm_image_name= filename.replace('top_mosaic','dsm').replace('png','tif').replace('area','matching_area')
        dsm_image= misc.imread(base_dir_dsm+"/"+dsm_image_name)
        print()
        print(np.shape(dsm_image))
        print(base_dir_dsm+"/"+dsm_image_name)
        ndsm_image_name= dsm_image_name.replace('.tif','')+"_normalized.jpg"
        ndsm_image= misc.imread(base_dir_ndsm+"/"+ndsm_image_name)
        print(np.shape(ndsm_image))
        print()
        width= np.shape(top_image)[1]
        height= np.shape(top_image)[0]
        for i in range(num_cropping_per_image):
            x = int(np.random.uniform(0, height - image_size + 1))
            y = int(np.random.uniform(0, width - image_size + 1))
            print((x,y))
            top_image_cropped= top_image[x:x + image_size, y:y + image_size, :]
            ndsm_image_cropped= ndsm_image[x:x + image_size, y:y + image_size]
            ndsm_image_cropped= np.expand_dims(ndsm_image_cropped,axis=2)
            dsm_image_cropped= dsm_image[x:x + image_size, y:y + image_size]
            dsm_image_cropped= np.expand_dims(dsm_image_cropped,axis=2)
            array_for_save= np.concatenate((top_image_cropped,ndsm_image_cropped,dsm_image_cropped),axis=2).astype(dtype=np.float16)
            np.save(os.path.join(base_dir_train, os.path.splitext(filename)[0] + "_" + str(i)+".npy"),array_for_save)
            #misc.imsave(os.path.join(base_dir_train, os.path.splitext(filename)[0] + "_" + str(i) + ".tif"), top_image_cropped)
            annotation_image_cropped= annotation_image[x:x + image_size, y:y + image_size]
            misc.imsave(os.path.join(base_dir_train_validate_gt, os.path.splitext(filename)[0] + "_" + str(i) + ".png"), annotation_image_cropped)
    return None


def create_validation_dataset():
    for filename in validate_image:
        top_image = misc.imread(os.path.join(base_dir_top, os.path.splitext(filename)[0] + ".tif"))
        annotation_image = misc.imread(os.path.join(base_dir_annotations, filename))
        dsm_image_name = filename.replace('top_mosaic', 'dsm').replace('png', 'tif').replace('area','matching_area')
        dsm_image = misc.imread(base_dir_dsm + "/" + dsm_image_name)
        ndsm_image_name = dsm_image_name.replace('.tif', '') + "_normalized.jpg"
        ndsm_image = misc.imread(base_dir_ndsm + "/" + ndsm_image_name)
        width = np.shape(top_image)[1]
        height = np.shape(top_image)[0]
        for i in range(num_cropping_per_image):
            x = int(np.random.uniform(0, height - image_size + 1))
            y = int(np.random.uniform(0, width - image_size + 1))
            print((x, y))
            top_image_cropped = top_image[x:x + image_size, y:y + image_size, :]
            ndsm_image_cropped = ndsm_image[x:x + image_size, y:y + image_size]
            ndsm_image_cropped = np.expand_dims(ndsm_image_cropped, axis=2)
            dsm_image_cropped = dsm_image[x:x + image_size, y:y + image_size]
            dsm_image_cropped = np.expand_dims(dsm_image_cropped, axis=2)
            array_for_save = np.concatenate((top_image_cropped, ndsm_image_cropped, dsm_image_cropped), axis=2).astype(dtype=np.float16)
            np.save(os.path.join(base_dir_validate, os.path.splitext(filename)[0] + "_" + str(i) + ".npy"), array_for_save)
            # misc.imsave(os.path.join(base_dir_train, os.path.splitext(filename)[0] + "_" + str(i) + ".tif"), top_image_cropped)
            annotation_image_cropped = annotation_image[x:x + image_size, y:y + image_size]
            misc.imsave(os.path.join(base_dir_train_validate_gt, os.path.splitext(filename)[0] + "_" + str(i) + ".png"),
                        annotation_image_cropped)
    return None

if __name__=="__main__":
    create_training_dataset()
