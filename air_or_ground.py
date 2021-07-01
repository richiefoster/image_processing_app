import os
import air_or_ground_error

def main():
    file1 = open('/home/ec2-user/air_or_ground.txt', 'r+')
    dir_var = file1.read()
    if str('air') in dir_var or str('Air') in dir_var:
        return 10
    elif str('ground') in dir_var or str('Ground') in dir_var:
        return 20
    else:
        return 400

if __name__ == '__main__':
    main()
    print(main())
    if main() != 10 or main() !=20:
        air_or_ground_error.main()
