import { Box, Button } from "@mui/material";
import Image from "next/image";
import React from "react";
import ImageUploading, { ImageListType } from "react-images-uploading";

interface imageUploaderProps {
  setImages: React.Dispatch<React.SetStateAction<ImageListType>>;
  maxNumber: number;
  images: ImageListType;
}
const ImageUploader = (props: imageUploaderProps) => {
  const { images, setImages, maxNumber } = props;
  console.log(images);
  const onChange = (
    imageList: ImageListType,
    addUpdateIndex: number[] | undefined
  ) => {
    setImages(imageList as never[]);
  };
  return (
    <ImageUploading
      multiple
      value={images}
      onChange={onChange}
      maxNumber={maxNumber}
    >
      {({
        imageList,
        onImageUpload,
        onImageRemoveAll,
        onImageUpdate,
        onImageRemove,
        isDragging,
        dragProps,
      }) => (
        // write your building UI
        <Box>
          {maxNumber > images.length ? (
            <Button
              style={isDragging ? { color: "red" } : undefined}
              onClick={onImageUpload}
              {...dragProps}
            >
              Click or Drop here
            </Button>
          ) : (
            <Button>더 올릴수 없어요</Button>
          )}
          &nbsp;
          <Button onClick={onImageRemoveAll}>Remove all images</Button>
          {`[${images.length} / ${maxNumber}]`}
          {imageList.map((image, index) => {
            return (
              <Box key={index}>
                <Image
                  src={image.dataURL ? image.dataURL : ""}
                  alt=""
                  width="200"
                  height="200"
                />
                <Box>
                  <Button onClick={() => onImageUpdate(index)}>Update</Button>
                  <Button onClick={() => onImageRemove(index)}>Remove</Button>
                </Box>
              </Box>
            );
          })}
        </Box>
      )}
    </ImageUploading>
  );
};

export default ImageUploader;
