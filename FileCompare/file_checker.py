import os
class FileComparison ():
    
    def __init__ (self):
        pass
    
    #compares file size and content
    def compare_files(self, file_1, file_2):
        """
            Compares two files byte by byte
            Returns True if the files match, false otherwise
        """
        #chunk size 
        chunk_size = 1024 
    
        try:
            file_1_size = os.path.getsize(file_1)
            file_2_size = os.path.getsize(file_2)
        
            #keeps track of bytes read
            file_size_read = 0
    
            # If two files do not have the same size, they cannot be same
            if file_1_size != file_2_size : 
                return False
    
            #if files are empty
            if file_2_size == 0:
                return True
    
            with open(file_1, "rb") as f1, open(file_2, "rb") as f2:
                
                    # Loops until the whole file has been read
                    while file_size_read <= file_1_size: 
                    
                    
                        # If the chunk of the file is not the same, the function returns false
                        if(f1.read(chunk_size) != f2.read(chunk_size)): 
                            return False

                        #adds chunk size to bytes read 
                        file_size_read += chunk_size

            #if file reading is over, returns True
            return True
    
        except:
            #if file path is Invalid
            print "File not found; Invalid Path"
            
        

