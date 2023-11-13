class cFormat():
    def format_number(number,decimal_places):
        try:
            num = float(number)
            if decimal_places == 0:
                return int( float( number ) )
            str_num = ("{:." + str( decimal_places ) + "f}").format(num)
            return float(str_num)
        except:
            return 0    