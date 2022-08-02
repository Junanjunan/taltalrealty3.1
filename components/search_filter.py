def search_filter(request):
    address = request.GET.get("address")
    guest_phone = request.GET.get("guest_phone")
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
    description = request.GET.get("description")

    filter_args = {}

    if address:
        filter_args["address__contains"] = address
    if guest_phone:
        filter_args["guest_phone__contains"] = guest_phone
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
    if parking == "on":
        filter_args["parking"] = True
    if elevator == "on":
        filter_args["elevator"] = True
    if loan == "on":
        filter_args["loan"] = True
    if empty == "on":
        filter_args["empty"] = True
    if not_finished == "on":
        filter_args["not_finished"] = True
    if naver == "on":
        filter_args["naver"] = True
    if dabang == "on":
        filter_args["dabang"] = True
    if zicbang == "on":
        filter_args["zicbang"] = True
    if peterpan == "on":
        filter_args["peterpan"] = True
    return filter_args