def setup_transparent_background(context, enable):
    scene = context.scene
    render = scene.render

    if enable:
        # Save for restore
        scene['previous_file_format'] = render.image_settings.file_format
        scene['previous_color_mode'] = render.image_settings.color_mode
        scene['previous_film_transparent'] = render.film_transparent
        # Change
        render.image_settings.file_format = 'PNG'
        render.image_settings.color_mode = 'RGBA'
        render.film_transparent = True
    else:
        # Restore unedited properties
        if render.image_settings.file_format == 'PNG':
            render.image_settings.file_format = scene.get(
                'previous_file_format', render.image_settings.file_format)
        if render.image_settings.color_mode == 'RGBA':
            render.image_settings.color_mode = scene.get(
                'previous_color_mode', render.image_settings.color_mode)
        if render.film_transparent:
            render.film_transparent = scene.get(
                'previous_film_transparent', render.film_transparent)
