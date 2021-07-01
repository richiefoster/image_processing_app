import os

def main():
    if not os.path.exists('/home'):
        os.mkdir('/home')
    else:
        pass
    if not os.path.exists('/home/ec2-user'):
        os.mkdir('/home/ec2-user')
    else:
        pass
    if not os.path.exists('/home/ec2-user/scripts'):
        os.mkdir('/home/ec2-user/scripts')
    else:
        pass
    os.chdir('/usr/src/app')

if __name__ == '__main__':
    main()

