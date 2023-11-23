def create(link):
    import qrcode
    data = "http://{}".format(link)
    filename = "{}.png".format(link.split('/')[1])
    img = qrcode.make(data)
    img.save(filename)


create('urbaton.ultraevs.ru/profile')