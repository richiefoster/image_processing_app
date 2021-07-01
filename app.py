import make_dirs
import download_images
import unzip
import process_images_ground
import zip_shp
import upload
import send_end_message
import cleanup
import time
import air_or_ground
import process_images_air

print('making dirs.....')
make_dirs.main()
print('next script: download_images')
download_images.main()
print('scirpt is sleeping for 3 minutes')
time.sleep(60)
print('awakening')
print('next script: unzip')
unzip.main()
# the script air_or_ground.py will decide which image processing script we need.
# 10 = air
# 20 = ground
# 400 = error
print('next script air_or_ground')
air_or_ground.main()
print(air_or_ground.main())
if air_or_ground.main() == 10:
    print('air_or_ground returned a value of 10, next script: process_images_air')
    process_images_air.main()
    zip_shp.main()
    upload.main()
    cleanup.main()
    send_end_message.main()
elif air_or_ground.main() == 20:
    print('air_or_ground returned a value of 20, next script: process_images_ground')
    process_images_ground.main()    
    zip_shp.main()
    upload.main()
    cleanup.main()
    send_end_message.main()


