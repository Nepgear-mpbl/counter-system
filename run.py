from counterSystem import create_app

if __name__ == '__main__':
    create_app('production').run()
    # create_app('development').run()