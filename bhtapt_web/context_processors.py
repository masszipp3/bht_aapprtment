def menu_context(request):
    current_url = request.resolver_match.url_name
    menu_items = [
           {'name': 'Dashboard', 'url': 'appartment:dashboard', 'icon': 'fa-tachometer-alt', 'url_name': 'dashboard'},
            {'name': 'Cash Book', 'url': 'appartment:cashbook', 'icon': 'fa-book', 'url_name': 'cashbook'},
            {'name': 'Bookings', 'url': 'appartment:bookingslist', 'icon': 'fa-chart-bar', 'url_name': 'bookingslist'},
            {'name': 'Cash Receipts', 'url': 'appartment:cashreciept_list', 'icon': 'fa-receipt', 'url_name': 'cashreciept_list'},
            {'name': 'Cash Payments', 'url': 'appartment:cash_payments', 'icon': 'fa-credit-card', 'url_name': 'cash_payments'},

            
    ]

    url_to_section = {
        'add_cashreciept': 'cashreciept_list',
        'reciept_edit': 'cashreciept_list',
        'cashreciept_print': 'cashreciept_list',
        'reciept_print': 'cashreciept_list',
        'bookingedit': 'bookingslist',
        'bookingdetail': 'bookingslist',
        'booking_reciept': 'bookingslist',
        'advance': 'bookingslist',
        'add_cashpayment': 'cash_payments',
        'edit_cashpayment': 'cash_payments',
        'add_cashpayment': 'cash_payments',
        'cashpayment_print': 'cash_payments',
        'add_account': 'Accounts',
        'edit_account': 'Accounts',
        'add_journal': 'journals',
        'edit_journal': 'journals',
        'booking': 'dashboard',
        'checkout': 'dashboard',
        'add_room': 'list_rooms',
        'edit_room': 'list_rooms',
        'room_Details': 'list_rooms',
        'addfloor': 'list_floors',
        'edit_floors': 'list_floors',
        'add_category': 'list_rooms',
        'edit_category': 'list_rooms',
        'add_user': 'users_list',
        'edit_user': 'users_list',
        'outstanding': 'reports',

    }

    # Determine the current section
    current_section = url_to_section.get(current_url, current_url)


    if request.user.is_superuser:
        menu_items.extend([
            {'name': 'Rooms', 'url': 'appartment:list_rooms', 'icon': 'fa-th', 'url_name': 'list_rooms'},
            {'name': 'Floors', 'url': 'appartment:list_floors', 'icon': 'fa-keyboard', 'url_name': 'list_floors'},
            {'name': 'Categories', 'url': 'appartment:list_category', 'icon': 'fa-table', 'url_name': 'list_category'},
            {'name': 'Accounts', 'url': 'appartment:accounts_list', 'icon': 'fa-address-book', 'url_name': 'accounts_list'},
            {'name': 'Journal', 'url': 'appartment:journals', 'icon': 'fa-random', 'url_name': 'journals'},
            {'name': 'Ledger', 'url': 'appartment:ledger', 'icon': 'fa-archive', 'url_name': 'ledger'}, 
            {'name': 'Users', 'url': 'appartment:users_list', 'icon': 'fa-user', 'url_name': 'users_list'},
            {'name': 'Reports', 'url': 'appartment:reports', 'icon': 'fa-list-alt ', 'url_name': 'reports'},

        ])


    return {
        'menu_items': menu_items,
         'current_url': current_section,
    }