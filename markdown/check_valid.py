import check_valid_img, check_valid_link

# 在上面两个脚本中, 都有对链接合法性的校测, 即必须以os.sep结尾, 所以下面使用的路径应该注意
DIRPATH = r"/home/netease/Projects/jyyslide-md/"

check_valid_img.DIRPATH = DIRPATH
check_valid_link.DIRPATH = DIRPATH

check_valid_img.check()
# check_valid_link.check()
