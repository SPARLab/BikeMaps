# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapApp', '0008_auto_20151207_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hazard',
            name='i_type',
            field=models.CharField(max_length=150, verbose_name='What type of hazard was it?', choices=[('Infrastructure', ((b'Curb', 'Curb'), (b'Island', 'Island'), (b'Train track', 'Train track'), (b'Pothole', 'Pothole'), (b'Road surface', 'Road surface'), (b'Poor signage', 'Poor signage'), (b'Speed limits', 'Speed limits'), (b'Blind corner', 'Blind corner or turn'), (b'Bike lane disappears', 'Bike lane disappears'), (b'Vehicles enter exit', 'Vehicles entering/exiting roadway'), (b'Dooring risk', 'Dooring risk zone'), (b'Vehicle in bike lane', 'Vehicle use of bike lane'), (b'Dangerous intersection', 'Dangerous intersection'), (b'Dangerous vehicle left turn', 'Dangerous vehicle left turn'), (b'Dangerous vehicle right turn', 'Dangerous vehicle right turn'), (b'Sensor does not detect bikes', 'Sensor does not pick up bikes'), (b'Steep hill', 'Steep hill - bike speed affected'), (b'Narrow road', 'Narrow road'), (b'Pedestrian conflict zone', 'Pedestrian conflict zone'), (b'Other infrastructure', 'Other (Please describe)'))), ('Environmental', ((b'Icy/Snowy', 'Icy/Snowy'), (b'Poor visibility', 'Poor visibility'), (b'Broken glass', 'Broken glass on road'), (b'Wet leaves', 'Wet leaves on road'), (b'Gravel rocks or debris', 'Gravel, rocks or debris on road/path'), (b'Construction', 'Construction'), (b'Other', 'Other (Please describe)'))), ('Human Behaviour', ((b'Poor visibility', 'Poor visibility'), (b'Parked car', 'Parked car'), (b'Traffic flow', 'Traffic flow'), (b'Driver behaviour', 'Driver behaviour'), (b'Cyclist behaviour', 'Cyclist behaviour'), (b'Pedestrian behaviour', 'Pedestrian behaviour'), (b'Congestion', 'Congestion'), (b'Other', 'Other (Please describe)')))]),
        ),
        migrations.AlterField(
            model_name='point',
            name='age',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='What is your birth year?', choices=[(b'2003', b'2003'), (b'2002', b'2002'), (b'2001', b'2001'), (b'2000', b'2000'), (b'1999', b'1999'), (b'1998', b'1998'), (b'1997', b'1997'), (b'1996', b'1996'), (b'1995', b'1995'), (b'1994', b'1994'), (b'1993', b'1993'), (b'1992', b'1992'), (b'1991', b'1991'), (b'1990', b'1990'), (b'1989', b'1989'), (b'1988', b'1988'), (b'1987', b'1987'), (b'1986', b'1986'), (b'1985', b'1985'), (b'1984', b'1984'), (b'1983', b'1983'), (b'1982', b'1982'), (b'1981', b'1981'), (b'1980', b'1980'), (b'1979', b'1979'), (b'1978', b'1978'), (b'1977', b'1977'), (b'1976', b'1976'), (b'1975', b'1975'), (b'1974', b'1974'), (b'1973', b'1973'), (b'1972', b'1972'), (b'1971', b'1971'), (b'1970', b'1970'), (b'1969', b'1969'), (b'1968', b'1968'), (b'1967', b'1967'), (b'1966', b'1966'), (b'1965', b'1965'), (b'1964', b'1964'), (b'1963', b'1963'), (b'1962', b'1962'), (b'1961', b'1961'), (b'1960', b'1960'), (b'1959', b'1959'), (b'1958', b'1958'), (b'1957', b'1957'), (b'1956', b'1956'), (b'1955', b'1955'), (b'1954', b'1954'), (b'1953', b'1953'), (b'1952', b'1952'), (b'1951', b'1951'), (b'1950', b'1950'), (b'1949', b'1949'), (b'1948', b'1948'), (b'1947', b'1947'), (b'1946', b'1946'), (b'1945', b'1945'), (b'1944', b'1944'), (b'1943', b'1943'), (b'1942', b'1942'), (b'1941', b'1941'), (b'1940', b'1940'), (b'1939', b'1939'), (b'1938', b'1938'), (b'1937', b'1937'), (b'1936', b'1936'), (b'1935', b'1935'), (b'1934', b'1934'), (b'1933', b'1933'), (b'1932', b'1932'), (b'1931', b'1931'), (b'1930', b'1930'), (b'1929', b'1929'), (b'1928', b'1928'), (b'1927', b'1927'), (b'1926', b'1926'), (b'1925', b'1925'), (b'1924', b'1924'), (b'1923', b'1923'), (b'1922', b'1922'), (b'1921', b'1921'), (b'1920', b'1920'), (b'1919', b'1919'), (b'1918', b'1918'), (b'1917', b'1917'), (b'1916', b'1916'), (b'1915', b'1915'), (b'1914', b'1914'), (b'1913', b'1913'), (b'1912', b'1912'), (b'1911', b'1911'), (b'1910', b'1910'), (b'1909', b'1909'), (b'1908', b'1908'), (b'1907', b'1907'), (b'1906', b'1906'), (b'1905', b'1905'), (b'1904', b'1904')]),
        ),
    ]
