from jinja2 import Template
import datetime

template = Template("""# Spatial crater count
#
# Date of measurement = {{date.strftime('%d/%m/%Y')}}
#
# Ellipsoid axes:
a_axis_radius = 3396.19 <km>
b_axis_radius = 3376.2 <km>
c_axis_radius = 3376.2 <km>
coordinate_system_name = unknown
#
# area_shapes:
unit_boundary = {vertex,sub_area,tag,lon,lat
#
# Area_name 1 = dl-ol
# Area_size 1 = {{counting_area}} <km^2>
#
1   1   ext 0   0
2   1   ext 0   0
3   1   ext 0   0
4   1   ext 0   0
}
#
Total_area = {{counting_area}} <km^2>
#
# crater_diameters:
crater = {diam, fraction, lon, lat
{% for key,value in craters.iterrows() -%}
{{value['diameter']}}   1   {{value['lon']}}    {{value['lat']}}
{% endfor -%}
}
""")


def create_scc_text(craters, counting_area):
    """
    Creates Spatial Crater Count format text using Jinja2 templating engine.

    arguments:
        craters - a DataFrame containing 'lat', 'lon', and 'area' columns
        area - the total counting area
    """
    # alternative implementation, using a `.j2` file
    # this doesn't work with ArcMap so instead we use
    # a string literal as defined above.
    # 
    # with open('scc_template.j2') as f:
    #     template = Template(f.read())
    return template.render(craters=craters, counting_area=counting_area, date=datetime.datetime.now())
    
