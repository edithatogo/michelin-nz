from std.sys import argv


comptime COUNTRY_SCALE = 100000.0
comptime GDP_SCALE = 10000000000.0


def stars_per_100k(total_stars: Float64, population: Float64) raises -> Float64:
    if population <= 0.0:
        raise "population must be positive"
    return (total_stars / population) * COUNTRY_SCALE


def gdp_per_capita(gdp: Float64, population: Float64) raises -> Float64:
    if population <= 0.0:
        raise "population must be positive"
    return gdp / population


def stars_per_10b_gdp(total_stars: Float64, gdp: Float64) raises -> Float64:
    if gdp <= 0.0:
        raise "gdp must be positive"
    return (total_stars / gdp) * GDP_SCALE


def main() raises:
    args = argv()
    if len(args) != 4:
        raise "usage: metrics.mojo <population> <gdp> <total_stars>"

    var population = atof(args[1])
    var gdp = atof(args[2])
    var total_stars = atof(args[3])

    print(
        stars_per_100k(total_stars, population),
        gdp_per_capita(gdp, population),
        stars_per_10b_gdp(total_stars, gdp),
    )
