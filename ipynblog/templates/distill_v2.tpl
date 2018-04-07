{%- extends 'display_priority.tpl' -%}

{%- block header -%}
<!DOCTYPE html>
<html>
<head>
    {%- block html_head -%}


    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://distill.pub/template.v2.js"></script>
    <style>
        <%= require("./style.css") %>
    </style>

    {% set nb_title = nb.metadata.get('title', '') or resources['metadata']['name'] %}
    <title>{{nb_title}}</title>

    {%- if "widgets" in nb.metadata -%}
    <script src="https://unpkg.com/jupyter-js-widgets@2.0.*/dist/embed.js"></script>
    {%- endif-%}

    {#    {% for css in resources.inlining.css -%}#}
    {#        <style type="text/css">#}
    {#            {{ css }}#}
    {#        </style>#}
    {#    {% endfor %}#}

    <!-- Loading mathjax macro -->
    {%- endblock html_head -%}
</head>
{%- endblock header -%}

{% block body %}
    <body>
    <d-article>
        {{ super() }}
    </d-article>
    </body>
{%- endblock body %}

{% block input %}


            <d-code block language="python" class="l-body" style="overflow: hidden; text-overflow: ellipsis;">
                {# no highlight_code #}
                {{ cell.source | ansi2html }}
            </d-code>


{%- endblock input %}

{% block markdowncell scoped %}


            <div class="l-body">
                {{ cell.source  | markdown2html | strip_files_prefix }}
            </div>


{%- endblock markdowncell %}


{% block output %}
    <div class="output_area" class="l-body">
        {{ super() }}
    </div>
{% endblock output %}

{% block stream_stdout -%}
    <div class="output_subarea output_stream output_stdout output_text">
        <pre>
            {{- output.text | ansi2html -}}
        </pre>
    </div>
{%- endblock stream_stdout %}

{% block stream_stderr -%}
    <div class="output_subarea output_stream output_stderr output_text">
        <pre>
            {{- output.text | ansi2html -}}
        </pre>
    </div>
{%- endblock stream_stderr %}


{% block execute_result -%}
    {%- set extra_class="output_execute_result" -%}
    {% block data_priority scoped %}
        {{ super() }}
    {% endblock data_priority %}
    {%- set extra_class="" -%}
{%- endblock execute_result %}


{% block data_png scoped %}
    <div class="output_png output_subarea {{ extra_class }}">
        {%- if 'image/png' in output.metadata.get('filenames', {}) %}
            <img src="{{ output.metadata.filenames['image/png'] | posix_path }}"
        {%- else %}
            <img src="data:image/png;base64,{{ output.data['image/png'] }}"
        {%- endif %}
        {%- set width=output | get_metadata('width', 'image/png') -%}
        {%- if width is not none %}
            width={{ width }}
        {%- endif %}
        {%- set height=output | get_metadata('height', 'image/png') -%}
        {%- if height is not none %}
            height={{ height }}
        {%- endif %}
        {%- if output | get_metadata('unconfined', 'image/png') %}
                 class="unconfined"
        {%- endif %}
        >
    </div>
{%- endblock data_png %}

{% block data_jpg scoped %}
    <div class="output_jpeg output_subarea {{ extra_class }}">
        {%- if 'image/jpeg' in output.metadata.get('filenames', {}) %}
            {# added the 'images/' here... #}
            <img src="images/{{ output.metadata.filenames['image/jpeg'] | posix_path }}"
        {%- else %}
            <img src="data:image/jpeg;base64,{{ output.data['image/jpeg'] }}"
        {%- endif %}
        {%- set width=output | get_metadata('width', 'image/jpeg') -%}
        {%- if width is not none %}
            width={{ width }}
        {%- endif %}
        {%- set height=output | get_metadata('height', 'image/jpeg') -%}
        {%- if height is not none %}
            height={{ height }}
        {%- endif %}
        {%- if output | get_metadata('unconfined', 'image/jpeg') %}
                 class="unconfined"
        {%- endif %}
        />
    </div>
{%- endblock data_jpg %}

{% block data_html scoped -%}
<div class="output_html rendered_html output_subarea {{ extra_class }}">
{{ output.data['text/html'] }}
</div>
{%- endblock data_html %}

