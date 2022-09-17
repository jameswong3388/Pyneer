import auth
import helpers

if __name__ == "__main__":
    a = helpers.existence_checker(key='id', value=1, table='foods')

    print(a)
