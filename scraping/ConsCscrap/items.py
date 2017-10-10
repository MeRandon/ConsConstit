from scrapy.item import Item, Field

class listCCitem(Item):
    dd = Field()
    mm = Field()
    yy = Field()
    num_dc = Field()
    type_dc = Field()
    objet_dc = Field()
    sol_dc = Field()
    publi_dc = Field()

    link_dc = Field()
    ecli_dc = Field()
    membres = Field()
