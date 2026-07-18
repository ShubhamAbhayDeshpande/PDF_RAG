"""
The program will take folder path for multiple pdf files as input and extract all the important data from the files
such as text, images, page numbers etc. and return a json file with all this data which can later be coverted to a 
python object. 

Creator: Shubham Deshpande
Version: 0.0

"""
import json
import os
import fitz


class pdf_parser:
    def __init__(self, pdf_folder_path):
        self.pdf_folder_path = pdf_folder_path
        self.save_parsed_json = True

        # Extract all paths to all PDFs in a list.
        self.files_list = []

        # Dictionary to store the document information.
        self.document_information = {}

        for root, _, files in os.walk(self.pdf_folder_path):
            for file in files:
                if file.endswith(".pdf") or file.endswith(".PDF"):
                    self.files_list.append(os.path.join(root, file))

    def get_page_information(self) -> dict:
        """
        Extract text and images from all PDFs in the configured folder.

        Returns:
            dict: A dictionary containing page-wise document information.
        """
        if self.document_information:
            self.document_information = {}

        for document in self.files_list:
            document_name = os.path.splitext(os.path.basename(document))[0]
            self.document_information[document_name] = {}

            with fitz.open(document) as doc:
                for page_number, page in enumerate(doc):
                    text = page.get_text()
                    page_info = {
                        "text": text,
                        "page_images": []
                    }

                    image_list = page.get_images(full=True)
                    if image_list:
                        for image in image_list:
                            xref = image[0]
                            image_width = image[2]
                            image_height = image[3]
                            image_bits = image[4]
                            image_color_space = image[5]

                            pix = fitz.Pixmap(doc, xref)
                            extracted_image_data = doc.extract_image(xref=xref)
                            

                            if pix.n - pix.alpha > 3:
                                pix = fitz.Pixmap(fitz.csRGB, pix)

                            image_name = f"{document_name}_image_{xref}.png"
                            os.makedirs("extracted_images", exist_ok=True)

                            image_path = os.path.join("extracted_images", image_name)
                            if not os.path.exists(image_path):
                                pix.save(image_path)

                            page_info["page_images"].append({
                                "xref": xref,
                                "image_width": image_width,
                                "image_height": image_height,
                                "image_bits": image_bits,
                                "image_color_space": image_color_space,
                                "x_resolution": extracted_image_data["xres"],
                                "y_resolution": extracted_image_data["yres"],
                                "image_path": image_path,
                            })

                            pix = None

                    self.document_information[document_name][page_number] = page_info

        if self.save_parsed_json:
            os.makedirs("jsondump", exist_ok=True)
            with open("jsondump/result.json", "w", encoding="utf-8") as fp:
                json.dump(self.document_information, fp, indent=4)

        return self.document_information
