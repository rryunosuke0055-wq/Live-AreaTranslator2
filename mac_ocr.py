import cv2
import numpy as np
import Quartz
import Vision
from CoreFoundation import CFURLCreateWithFileSystemPath, kCFAllocatorDefault, kCFURLPOSIXPathStyle
import time

def extract_text_mac(image_bgr):
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    height, width, _ = image_rgb.shape
    
    # Needs to be wrapped in NSData or CGImage
    # An easier way is to save it to a temporary file, then read it via NSURL
    tmp_path = "/tmp/ocr_temp.png"
    cv2.imwrite(tmp_path, image_bgr)
    
    req = Vision.VNRecognizeTextRequest.alloc().init()
    req.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    
    # 認識言語を日本語・英語に指定
    req.setRecognitionLanguages_(["ja-JP", "en-US"])
    
    url = Quartz.NSURL.fileURLWithPath_(tmp_path)
    handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(url, None)
    
    success, error = handler.performRequests_error_([req], None)
    if success:
        results = req.results()
        text = "\n".join([res.topCandidates_(1)[0].string() for res in results])
        return text
    return ""

if __name__ == "__main__":
    # dummy image with text
    img = np.zeros((100, 300, 3), dtype=np.uint8)
    img.fill(255)
    cv2.putText(img, "Hello World from Mac OCR!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
    
    t0 = time.time()
    print("Extracting...")
    text = extract_text_mac(img)
    t1 = time.time()
    print(f"Result: {text}")
    print(f"Time: {t1-t0}s")
