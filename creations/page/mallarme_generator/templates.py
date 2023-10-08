SVG_TEXT = """
    <text
       xml:space="preserve"
       id="{id}"
       class="{_class}"
       style="{style}"
       >
       <tspan
         x={x}
         y={y}
         id="tspan{id}">{text}</tspan>
    </text>
"""


SVG_PATH = """
    <path
       style="{style}"
       d="m {x},{y} c -0.111428,-0.05274 1.671755,-6.162561 9.525248,-11.372959 3.581504,-2.375634 8.498707,-4.348567 14.249445,-4.515956 4.687609,-0.135831 9.857869,0.976948 14.529509,3.687029 4.198651,2.436516 7.936536,6.14057 10.426069,10.797947 0.470616,0.883345 0.892921,1.789496 1.282916,2.714733 1.287698,3.054974 2.180102,6.184551 3.237715,9.124676 1.503679,4.138661 3.333733,7.881958 6.308183,10.492772 2.571506,2.274138 5.808564,3.498344 8.896524,3.694998 0,0 4e-6,-10e-7 4e-6,-10e-7 3.529372,0.22625 6.836413,-0.85546 9.325423,-2.542613"
       id="path{id}"
       class="{_class}"
       inkscape:path-effect="{effects}#path-effect-spiro;#path-effect-skeletal"
       inkscape:original-d="M {x},{y} C 43.000223,35.802408 59.09702,35.412722 75.193553,35.022774 91.290086,34.632823 82.500924,49.988361 86.154211,57.470756 89.807499,64.953154 102.41447,46.273981 110.5442,40.675197" />
"""

SVG_FILE = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>

<svg
   width="2100mm"
   height="2970mm"
   viewBox="0 0 2100 2970"
   version="1.1"
   id="svg39095"
   inkscape:version="1.1.2 (0a00cf5339, 2022-02-04)"
   sodipodi:docname="path_only.svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <sodipodi:namedview
     id="namedview39097"
     pagecolor="#ffffff"
     bordercolor="#666666"
     borderopacity="1.0"
     inkscape:pageshadow="2"
     inkscape:pageopacity="0.0"
     inkscape:pagecheckerboard="0"
     inkscape:document-units="mm"
     showgrid="false"
     inkscape:zoom="0.69664703"
     inkscape:cx="396.18342"
     inkscape:cy="560.54212"
     inkscape:window-width="1920"
     inkscape:window-height="1016"
     inkscape:window-x="0"
     inkscape:window-y="0"
     inkscape:window-maximized="1"
     inkscape:current-layer="layer1" />
  <defs
     id="defs39092">
    <inkscape:path-effect
       effect="skeletal"
       id="path-effect-skeletal"
       is_visible="true"
       lpeversion="1"
       pattern="M 0,4.9921382 C 0,2.2364779 2.2364779,0 4.9921382,0 c 2.7556604,0 4.9921383,2.2364779 4.9921383,4.9921382 0,2.7556604 -2.2364779,4.9921383 -4.9921383,4.9921383 C 2.2364779,9.9842765 0,7.7477986 0,4.9921382"
       copytype="single_stretched"
       prop_scale="0.1"
       scale_y_rel="false"
       spacing="0"
       normal_offset="0"
       tang_offset="0"
       prop_units="false"
       vertical_pattern="false"
       hide_knot="false"
       fuse_tolerance="0" />
    <inkscape:path-effect
       effect="spiro"
       id="path-effect-spiro"
       is_visible="true"
       lpeversion="1" />
  </defs>
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">
    {elements}
  </g>

</svg>
"""

HTML_FILE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  .text_rendering {{
    opacity: 0;
  }}

  .path_rendering {{
    opacity: 0; 
    visibility: hidden;
    stroke: #37abc8;
    stroke-dasharray: 1000;
    stroke-dashoffset: 0; 
    animation: drawPath 3s linear forwards;
  }}

  @keyframes drawPath {{
    0% {{
      stroke-dashoffset: 1000;
      opacity: 0; 
      visibility: hidden; 
    }}
    50% {{
      stroke-dashoffset: 0;
      opacity: 1; 
      visibility: visible; 
    }}
    100% {{
      stroke-dashoffset: -1000;
      opacity: 0; 
      visibility: hidden; 
    }}
  }}


  @keyframes fadeInStayOut {{
  0% {{
    opacity: 0;
  }}
  5% {{
    opacity: 0.5;
  }}
  10% {{
    opacity: 0.75;
  }}
  15% {{
    opacity: 1.00;
  }}
  20% {{
    opacity: 0.9;
  }}
  25% {{
    opacity: 0.7;
  }}
  50% {{
    opacity: 0.5;
  }}
  75% {{
    opacity: 0.35; 
  }}
  90% {{
    opacity: 0.2;
  }}
  100% {{
    opacity: 0; 
  }}
}}

.fade-in-stay-out {{
  animation: fadeInStayOut 3s linear ; 
}}

{css_animation_delaies}

</style>
</head>
<body>
  <div class="svg-container">
  {svg_content}
  </div>
</body>
</html>
"""

CSS_DELAY = """
.second_delay_{delay_name} {{
    animation-delay: {delay}s;
}}
"""
