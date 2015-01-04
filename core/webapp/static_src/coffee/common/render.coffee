render_all = ->
    if mode.current == mode.USER
        render_user()
    else if mode.current == mode.FABSCRIPT
        render_fabscript()
    else if mode.current == mode.RESULT
        render_result()
    else if mode.current == mode.NODE
        render_node()


init = ->
    $('[data-toggle=popover]').popover()

    $('#show-graph').on('click', ->
        $('#graph-modal').modal()
        return)

    $('#graph-modal').on('shown.bs.modal', ->
        render_force_layout()
        return)

    $('#search-input').on('change', filter)
                      .on('keyup', filter)

    $('#all-checkbox').on('change', ->
        is_checked = $(this).prop('checked')
        trs = $('tbody > tr')
        for tr in trs
            tr = $(tr)
            if tr.is(':visible')
                tr.find('input[type=checkbox]').prop('checked', is_checked)
            else
                tr.find('input[type=checkbox]').prop('checked', false)
        return)

    users = $('#users')
    if users.length > 0
        mode.current = mode.USER
        users = JSON.parse(users.html())

    nodes = $('#nodes')
    if nodes.length > 0
        mode.current = mode.NODE
        nodes = JSON.parse(nodes.html())

    node_clusters = $('#node_clusters')
    if node_clusters.length > 0
        node_clusters = JSON.parse(node_clusters.html())

    fabscripts = $('#fabscripts')
    if fabscripts.length > 0
        mode.current = mode.FABSCRIPT
        fabscripts = JSON.parse(fabscripts.html())
        for fabscript in fabscripts
            fabscript.fields.link = JSON.parse(fabscript.fields.link)
            fabscript.fields.linked_fabscripts = JSON.parse(fabscript.fields.linked_fabscripts)

    results = $('#results')
    if results.length > 0
        mode.current = mode.RESULT
        results = JSON.parse(results.html())

    render_all()

    if $.support.pjax
        $(document).pjax('.pjax', '#pjax-container')
        $(document).on('pjax:end', ->
            pathname = location.pathname.split('/', 2)
            $('.pjax').parent().removeClass('active')
            $('a[href="/' + pathname[1] + '/"]').parent().addClass('active')
            init()
            return)

    $(window).on('hashchange', ->
        render_all()
        return)

    return


init()
