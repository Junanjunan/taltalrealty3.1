def search_filter_for_app(request):
    realtor_id = request.GET.get("realtor_id")
    address = request.GET.get("address")
    guest_phone = request.GET.get("guest_phone")
    price = request.GET.get("price")
    deposit = request.GET.get("deposit")
    month_fee = request.GET.get("month_fee")
    room = request.GET.get("room")
    area_m2 = request.GET.get("area_m2")
    land_m2 = request.GET.get("land_m2")
    parking = request.GET.get("parking")
    elevator = request.GET.get("elevator")
    loan = request.GET.get("loan")
    empty = request.GET.get("empty")
    not_finished = request.GET.get("not_finished")
    naver = request.GET.get("naver")
    dabang = request.GET.get("dabang")
    zicbang = request.GET.get("zicbang")
    peterpan = request.GET.get("peterpan")
    report = request.GET.get("report")
    deal_report = request.GET.get("deal_report")
    deal_renewal_notice = request.GET.get("deal_renewal_notice")
    deal_renewal_right_usage = request.GET.get("deal_renewal_right_usage")
    description = request.GET.get("description")

    filter_args = {}
    
    filter_args["realtor_id"] = int(realtor_id)
    if address:
        filter_args["address__contains"] = address
    if guest_phone:
        filter_args["guest_phone__contains"] = guest_phone
    if price:
        filter_args["price__lte"] = price
    if deposit:
        filter_args["deposit__lte"] = deposit
    if month_fee:
        filter_args["month_fee__lte"] = month_fee
    if area_m2:
        filter_args["area_m2__gte"] = area_m2
    if land_m2:
        filter_args["land_m2__gte"] = land_m2
    if room:
        filter_args["room__gte"] = room
    if description:
        filter_args["description__contains"] = description
    if parking:
        filter_args["parking"] = True
    if elevator:
        filter_args["elevator"] = True
    if loan:
        filter_args["loan"] = True
    if empty:
        filter_args["empty"] = True
    if not_finished:
        filter_args["not_finished"] = True
    if naver:
        filter_args["naver"] = True
    if dabang:
        filter_args["dabang"] = True
    if zicbang:
        filter_args["zicbang"] = True
    if peterpan:
        filter_args["peterpan"] = True
    if report:
        filter_args["report"] = True
    if deal_report:
        filter_args["deal_report"] = True
    if deal_renewal_notice:
        filter_args["deal_renewal_notice"] = True
    if deal_renewal_right_usage:
        filter_args["deal_renewal_right_usage"] = True
    return filter_args