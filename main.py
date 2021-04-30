from tornado.httpclient import HTTPClient
import tornado.web
import tornado.ioloop
import scraperTornado
import os


class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.html")


class searchHandler(tornado.web.RequestHandler):
    def get(self):
        product = self.get_argument("prod")
        # product contains actual space, not '+' or '%20'
        print("In main.py: ", product)

        amazonlist = scraperTornado.searchProductAmazon(product)
        flipkartlist = scraperTornado.searchProductFlipkart(product)
        snapdeallist = scraperTornado.searchProductSnapdeal(product)

        p = [amazonlist,flipkartlist,snapdeallist]
        products = []
        for i in p:
            if i is not None:
                products += i

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
    port = int(os.environ.get("PORT", 8882))
    app.listen(port)  # port number is a string.
    print("Listening on 8882..")
    tornado.ioloop.IOLoop.current().start()
