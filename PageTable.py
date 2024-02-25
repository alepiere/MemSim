class PageTable:

    def __init__(self, page_size, num_pages, num_frames):
        self.page_size = page_size
        self.num_pages = num_pages
        self.num_frames = num_frames
        self.page_table = [None] * num_pages

    # def get_frame(self, page_num):
    #     return self.page_table[page_num]

    # def set_frame(self, page_num, frame_num):
    #     self.page_table[page_num] = frame_num

    # def __str__(self):
    #     return str(self.page_table)