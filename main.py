from tornado.httpclient import HTTPClient
import tornado.web
import tornado.ioloop
import scraperTornado


class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")


class searchHandler(tornado.web.RequestHandler):
    def get(self):
        product = self.get_argument("prod")
        #products = product.objects.filter(name__icontains=srh)
        #params = {'products': products, 'search': srh}
        products = scraperTornado.searchProductAmazon(product)+\
                  scraperTornado.searchProductFlipkart(product)+scraperTornado.searchProductSnapdeal(product)

        try:
            products.sort(key=lambda x: (x[5],-x[4]))  # Sort according to PRICE then if PRICE is same, sort according to decreasing number of ratings.
        except:
            pass

        products2 = []
        for i in products:
            product = (i[0], i[1], i[2], str(i[3]), str(i[4]), str(i[5]))
            # print(product)
            products2.append(product)

        self.render("search.html", products=products2)


app = tornado.web.Application([
    (r"/", basicRequestHandler),
    (r"/search", searchHandler),
])


if __name__ == "__main__":
    app.listen("8882")
    print("Listening on 8882..")
    tornado.ioloop.IOLoop.current().start()
