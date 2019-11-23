
def sub(data, page=1, limit=30):
    """
    paging json
    expect param as list
    """
    total = len(data)
    total_page = total // limit
    if page == 0: page = 1
    if total_page == 0: total_page = 1
    skip = limit * (page - 1)
    return {
        'total': total,
        'total_page': total_page,
        'data': data[skip:page * limit]
    }
