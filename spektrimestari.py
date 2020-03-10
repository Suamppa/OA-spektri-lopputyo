import ikkunasto
import numpy
import os

from tkinter import filedialog

VERSIO = "1.1.0"

# Ikkunasto-moduulin luonteen vuoksi käyttöliittymän elementit täytyy saada globaalisti saataville.
ELEMENTIT = {
    "akselit": None,
    "intensiteettinappi": False,
    "kuvaaja": None,
    "piirtoalue": None,
    "poistonappi": False,
    "suhdenappi": False,
    "tallennusnappi": False,
    "tekstilaatikko": None,
    "vasen_yla_kehys": None,
}

# Käsiteltävän datan listat tarvitaan globaalisti saataville.
LISTAT = {
    "energiat": [],
    "intensiteetit": [],
    "ladatut": 0,
    "piikkien_I": [],
    "pisteet": [],
    "virheelliset": [],
}

def nayta_ohje():
    """
    Napinkäsittelijä, joka näyttää ohjeikkunan ohjelman eri toiminnoista.
    """
    
    ohje_otsikko = (
        "Tämä ohje kuvailee ohjelman eri toiminnot.\n"
        "Suurin osa toimintojen napeista tulee näkyviin vasta, kun niitä voidaan käyttää.\n"
    )
    avaa_ohje = (
        "Avaa ikkunan, jossa voit valita kansion, joka sisältää käsiteltävän mittausdatan.\n"
        "Tiedoston nimen tulee olla muotoa \"measurement_x.txt\", missä \"x\" on kokonaisluku.\n"
        "Tiedoston sisällön täytyy olla muotoa \"E I\",\n"
        "missä E on sidosenergia ja I on sitä vastaava intensiteetti.\n"
        "Arvot on erotettu välilyönnillä ja jokainen pari on omalla rivillään.\n"
    )
    tallenna_ohje = (
        "Tallentaa nykyisen kuvaajan valitsemassasi muodossa.\n"
        "Yleisimmät tuetut tiedostotyypit on listattu tallennusikkunan pudotuslistassa.\n"
        "Kaikki ohjelman tukemat tiedostopäätteet on listattu alla:\n"
        ".eps, .jpeg, .jpg, .pdf, .pgf, .png, .ps, .raw, .rgba, .svg, .svgz, .tif, .tiff\n"
    )
    poista_tausta_ohje = (
        "Poistaa spektristä mittauslaitteistosta johtuvan lineaarisen taustan.\n"
        "Valitse kaksi pistettä kuvaajan alku- ja loppupäästä klikkaamalla.\n"
        "Niiden välille sovitetaan suora.\n"
        "Tämän jälkeen spektrin jokaisesta pisteestä vähennetään samaa energiaa "
        "vastaava suoran arvo,\nmikä tasoittaa kuvaajan, jos pisteet on valittu oikein.\n"
    )
    intensiteetti_ohje = (
        "Laskee halutun piikin intensiteetin.\n"
        "Rajaa piikin energiaväli valitsemalla kaksi pistettä.\n"
        "Piikin intensiteetti saadaan laskemalla sen pinta-ala integroimalla.\n"
        "Integroinnissa käytetään puolisuunnikassääntöä.\n"
    )
    suhde_ohje = (
        "Ilmoittaa kahden viimeksi mitatun intensiteettipiikin välisen suhteen.\n"
        "Suhde tulostuu tekstilaatikkoon.\n"
    )
    ohje_ohje = "Avaa tämän ikkunan.\n"
    tyhjenna_ohje = "Tyhjentää ohjelman muistin ja palauttaa sen alkutilaan.\n"
    lopeta_ohje = "Sulkee ohjelman.\n"
    
    ohjeikkuna = ikkunasto.luo_ali_ikkuna("Ohje")
    ohje_tekstilaatikko = ikkunasto.luo_tekstilaatikko(ohjeikkuna, 92, 43)
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, ohje_otsikko)
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, "Avaa:")
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, avaa_ohje)
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, "Tallenna:")
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, tallenna_ohje)
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, "Poista tausta:")
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, poista_tausta_ohje)
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, "Intensiteetti:")
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, intensiteetti_ohje)
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, "Suhde:")
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, suhde_ohje)
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, "Ohje:")
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, ohje_ohje)
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, "Tyhjennä:")
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, tyhjenna_ohje)
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, "Lopeta:")
    ikkunasto.kirjoita_tekstilaatikkoon(ohje_tekstilaatikko, lopeta_ohje)

def tallenna_kuvaaja():
    """
    Napinkäsittelijä, joka tallentaa nykyisen kuvaajan .png-muodossa.
    Polun määrittely perustuu ikkunasto-moduulin avaa_tallennusikkuna-funktioon,
    mutta siihen on lisätty argumentteja, jotka löytyvät tkinter-dokumentaatiosta:
    https://infohost.nmt.edu/tcc/help/pubs/tkinter/web/tkFileDialog.html
    """
    
    polku = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG", ".png"), ("JPEG", ".jpg"), ("TIFF", ".tif"), ("PDF", ".pdf")],
        initialdir=".",
        title="Tallenna kuvaaja"
    )
    if polku:
        try:
            ELEMENTIT["kuvaaja"].savefig(polku)
        except ValueError:
            ikkunasto.avaa_viesti_ikkuna("Tallennus epäonnistui", "Tiedostotyyppiä ei tueta.", True)
        else:
            tallennusotsikko = "Kuvaaja tallennettu"
            tallennusviesti = "Kuvaaja tallennettu nimellä {}"
            tallennusteksti = "Kuvaaja tallennettu kohteeseen:\n{}"
            tiedostonimi = polku.rsplit("/", 1)
            ikkunasto.avaa_viesti_ikkuna(tallennusotsikko, tallennusviesti.format(tiedostonimi[1]))
            ikkunasto.kirjoita_tekstilaatikkoon(
                ELEMENTIT["tekstilaatikko"], tallennusteksti.format(tiedostonimi[0])
            )

def piikkien_suhde():
    """
    Napinkäsittelijä, joka selvittää kahden viimeksi lasketun intensiteettipiikin suhteen.
    Tulostaa lopuksi montako kertaa suurempi suurempi piikki on.
    """
    
    piikit = LISTAT["piikkien_I"][:]
    piikit.sort()
    pieni_piikki = piikit[0]
    suuri_piikki = piikit[1]
    if pieni_piikki == suuri_piikki:
        suhdeviesti = "Intensiteetit ovat yhtä suuret. Mielenkiintoista..."
        ikkunasto.kirjoita_tekstilaatikkoon(ELEMENTIT["tekstilaatikko"], suhdeviesti)
    elif pieni_piikki == 0:
        virhe_otsikko = "Virhe suhteen määrittämisessä"
        virheviesti = "Toinen intensiteetti ei voi olla nolla!"
        ikkunasto.avaa_viesti_ikkuna(virhe_otsikko, virheviesti, True)
    else:
        suhde = suuri_piikki / pieni_piikki
        suhdeviesti = "Suurempi piikki on {:.3f} kertaa pienempää suurempi.".format(suhde)
        ikkunasto.kirjoita_tekstilaatikkoon(ELEMENTIT["tekstilaatikko"], suhdeviesti)

def piikin_intensiteetti(alku, loppu):
    """
    Laskee integroimalla piikin intensiteetin käyttäen
    puolisuunnikassääntöä annetulla energiavälillä.
    Tämä toteutetaan käyttäen numpy-kirjaston trapz-funktiota.
    Luo lopuksi piikkien suhteen laskemisnapin, jos sitä ei vielä ole.
    
    :param int alku: indeksi, jonka perusteella löydetään piikin alkupiste
    :param int loppu: indeksi, jonka perusteella löydetään piikin loppupiste
    """
    
    otsikko = "Lasketaan piikin intensiteetti"
    ilmoitus = "Lasketaan piikin intensiteetti käyttäen energiaväliä\n"
    energiavali = "{:.3f} eV - {:.3f} eV".format(LISTAT["energiat"][alku], LISTAT["energiat"][loppu])
    ikkunasto.avaa_viesti_ikkuna(otsikko, ilmoitus + energiavali + ".")
    intensiteetti = numpy.trapz(LISTAT["intensiteetit"][alku:loppu], LISTAT["energiat"][alku:loppu])
    if len(LISTAT["piikkien_I"]) >= 2:
        LISTAT["piikkien_I"].remove(LISTAT["piikkien_I"][0])
    LISTAT["piikkien_I"].append(intensiteetti)
    intensiteetti_ilmoitus = (
        "Intensiteetti energiavälillä {} on {:.3f}.".format(energiavali, intensiteetti)
    )
    ikkunasto.kirjoita_tekstilaatikkoon(ELEMENTIT["tekstilaatikko"], intensiteetti_ilmoitus)
    LISTAT["pisteet"] = []
    if len(LISTAT["piikkien_I"]) >= 2 and not ELEMENTIT["suhdenappi"]:
        ELEMENTIT["suhdenappi"] = ikkunasto.luo_nappi(
            ELEMENTIT["vasen_yla_kehys"], "Suhde", piikkien_suhde
        )

def valmistele_intensiteetti():
    """
    Napinkäsittelijä, joka suorittaa tarvittavat valmistelut intensiteettilaskentaa varten.
    Luo valittujen pisteiden perusteella aloitus- ja lopetusindeksin piikin rajaamiseksi.
    Indeksit välitetään piikin_intensiteetti-funktiolle.
    """
    
    virhe_otsikko = "Intensiteetin laskeminen epäonnistui"
    valintaohje = "Valitse energiaväli klikkaamalla."
    minimivali = (
        numpy.abs(LISTAT["energiat"][-1] - LISTAT["energiat"][0]) / len(LISTAT["energiat"])
    )
    x1, y1, x2, y2 = tarkista_pisteet(virhe_otsikko, valintaohje, minimivali)
    if x1 == None and y1 == None and x2 == None and y2 == None:
        pass
    else:
        alkuindeksi = -1
        loppuindeksi = -1
        for i, E in enumerate(LISTAT["energiat"]):
            if E >= x1:
                alkuindeksi = i
                break
        for i, E in enumerate(LISTAT["energiat"]):
            if E > x2:
                loppuindeksi = i - 1
                break
        if alkuindeksi == -1 or loppuindeksi == -1:
            virheviesti = "Energiavälin määritys epäonnistui."
            ikkunasto.avaa_viesti_ikkuna(virhe_otsikko, virheviesti, True)
        else:
            piikin_intensiteetti(alkuindeksi, loppuindeksi)

def laske_parametrit(x1, y1, x2, y2):
    """
    Laskee annettujen pisteiden välisen suoran kulmakertoimen ja vakiotermin.
    Jos kulmakerrointa ei ole, palauttaa kaksi Nonea.
    
    :param float x1, y1, x2, y2: käytettävät pisteet
    :return: kulmakerroin k, vakiotermi b
    """
    
    try:
        k = (y2 - y1) / (x2 - x1)
    except ZeroDivisionError:
    #Tätähän ei olemassa olevilla ehdoilla pitäisi saada aikaan, mutta varmistetaan.
        ilmoitus = (
            "Pisteiden ({x1:.3f}, {y1:.3f}) ja ({x2:.3f}, {y2:.3f}) "
            "kautta kulkeva suora on pystysuora, ei kulmakerrointa. "
            "Valitse toiset pisteet.".format(x1=x1, y1=y1, x2=x2, y2=y2)
        )
        ikkunasto.avaa_viesti_ikkuna("Ei kulmakerrointa", ilmoitus, True)
        return None, None
    else:
        b = (x2 * y1 - x1 * y2) / (x2 - x1)
        return k, b

def laske_pisteet_suoralla(k, b, x_pisteet):
    """
    Tuottaa joukon pisteitä, jotka ovat annetulla kulmakertoimella ja
    vakiotermillä määritetyn suoran arvoja annetuissa x-akselin pisteissä.
    
    :param float k: kulmakerroin
    :param float b: vakiotermi
    :param list x_pisteet: lista käytettäviä x-akselin pisteitä
    :return: lista x-pisteitä vastaavia suoran arvoja
    """
    
    arvot = []
    for x in x_pisteet:
        arvot.append(k * x + b)
    return arvot

def poista_tausta():
    """
    Napinkäsittelijä, joka poistaa spektristä mittauslaitteistosta johtuvan lineaarisen taustan.
    Käyttäjälle ilmoitetaan, mitä pisteitä tullaan käyttämään.
    Luo lopuksi intensiteetin laskemisnapin, jos sitä ei vielä ole.
    
    :param float x1, y1, x2, y2: pisteet, joiden välille sovitetaan suora
    """
    
    virhe_otsikko = "Lineaarisen taustan poistaminen epäonnistui"
    valintaohje = "Valitse kuvaajan alku- ja loppupäästä kaksi pistettä klikkaamalla."
    minimivali = numpy.abs(LISTAT["energiat"][-1] - LISTAT["energiat"][0]) / 4
    x1, y1, x2, y2 = tarkista_pisteet(virhe_otsikko, valintaohje, minimivali)
    if x1 == None and y1 == None and x2 == None and y2 == None:
    # Tässähän voisi tarkistaa vain yhden näistä Noneksi, mutta perfektionismi.
        pass
    else:
        poisto_otsikko = "Poistetaan lineaarinen tausta"
        poistoilmoitus = "Poistetaan lineaarinen tausta käyttäen pisteitä\n"
        pisteet = (
            "({x1:.3f}, {y1:.3f}) ja ({x2:.3f}, {y2:.3f})."
            .format(x1=x1, y1=y1, x2=x2, y2=y2)
        )
        ikkunasto.avaa_viesti_ikkuna(poisto_otsikko, poistoilmoitus + pisteet)
        k, b = laske_parametrit(x1, y1, x2, y2)
        if k == None:
            # Tämä ilmoitus tulee ainoastaan tekstilaatikkoon,
            # koska siitä avataan viesti-ikkuna jo laske_parametrit-funktion sisällä.
            ikkunasto.kirjoita_tekstilaatikkoon(ELEMENTIT["tekstilaatikko"], virhe_otsikko)
        else:
            suoran_arvot = laske_pisteet_suoralla(k, b, LISTAT["energiat"])
            for i, y in enumerate(suoran_arvot):
                LISTAT["intensiteetit"][i] = LISTAT["intensiteetit"][i] - y
            kuittaus = "Lineaarinen tausta poistettu käyttäen pisteitä:\n"
            ikkunasto.kirjoita_tekstilaatikkoon(ELEMENTIT["tekstilaatikko"], kuittaus + pisteet)
            piirra_data()
            LISTAT["pisteet"] = []
            if not ELEMENTIT["intensiteettinappi"]:
                ELEMENTIT["intensiteettinappi"] = ikkunasto.luo_nappi(
                    ELEMENTIT["vasen_yla_kehys"], "Intensiteetti", valmistele_intensiteetti
                )

def tarkista_pisteet(virhe_otsikko, virheviesti, minimivali=0):
    """
    Tarkistaa, onko piirretystä kuvaajasta valittu kaksi kelvollista pistettä.
    Huono tai puuttuva piste palauttaa neljä Nonea ja tulostaa asianmukaisen virheikkunan
    käyttäen annettua otsikkoa ja puuttuvien pisteiden tapauksessa viestiä.
    Valinnainen argumentti minimivali määrittää pienimmän sallitun etäisyyden pisteiden
    välillä x-akselilla.
    
    :param str virhe_otsikko: virheikkunan otsikko
    :param str virheviesti: virheikkunan teksti
    :param float minimivali: pienin sallittu pisteiden etäisyys x-akselilla
    :return: kaksi koordinaattipistettä, virheestä neljä Nonea
    """
    
    pisteet = LISTAT["pisteet"][:]
    pisteet.sort()
    try:
        x1, y1 = pisteet[0]
        x2, y2 = pisteet[1]
    except IndexError:
        ikkunasto.avaa_viesti_ikkuna(virhe_otsikko, virheviesti, True)
        return None, None, None, None
    except TypeError:
        ikkunasto.avaa_viesti_ikkuna(virhe_otsikko, virheviesti, True)
        return None, None, None, None
    else:
        if numpy.abs(x2 - x1) < minimivali:
            etaisyysohje = ("Valitse toisistaan kauempana olevat pisteet.")
            ikkunasto.avaa_viesti_ikkuna(virhe_otsikko, etaisyysohje, True)
            return None, None, None, None
        else:
            return x1, y1, x2, y2

def valitse_datapiste(tapahtuma):
    """
    Ottaa vastaan hiiren klikkaustapahtuman ja lukee siitä datapisteen x- ja y-arvot.
    Klikkaus määrittää käytetyn x-pisteen.
    Arvot tulosteetaan tekstilaatikkoon sekä
    talletetaan ohjelman listat-sanakirjassa olevaan pisteet-listaan.
    Pisteet-listassa säilytetään kerralla enintään kahta pisteparimonikkoa.
    
    :param MouseEvent tapahtuma: klikkaustapahtuma
    """
    
    if tapahtuma.button == 1:
        x_arvo = tapahtuma.xdata
        y_arvo = tapahtuma.ydata
        tuloste = "Arvo pisteessä x={:.3f} on {:.3f}".format(x_arvo, y_arvo)
        ikkunasto.paivita_tekstirivi(ELEMENTIT["tekstirivi"], tuloste)
        if len(LISTAT["pisteet"]) >= 2:
            LISTAT["pisteet"].remove(LISTAT["pisteet"][0])
        LISTAT["pisteet"].append((x_arvo, y_arvo))

def piirra_data():
    """
    Piirtää sen hetkisen ohjelman muistista löytyvän datan näkyviin.
    Luo lopuksi lineaarisen taustan poistonapin sekä tallennusnapin,
    jos niitä ei vielä ole.
    """
    
    ELEMENTIT["akselit"].cla()
    ELEMENTIT["akselit"].set_xlabel("Sidosenergia (eV)")
    ELEMENTIT["akselit"].set_ylabel("Intensiteetti (mielivaltainen yksikkö)")
    ELEMENTIT["akselit"].grid(True)
    ELEMENTIT["akselit"].plot(LISTAT["energiat"], LISTAT["intensiteetit"])
    ELEMENTIT["piirtoalue"].draw()
    piirtoilmoitus = "Nykyinen data piirretty."
    ikkunasto.kirjoita_tekstilaatikkoon(ELEMENTIT["tekstilaatikko"], piirtoilmoitus)
    ikkunasto.paivita_tekstirivi(ELEMENTIT["tekstirivi"], "Valitse piste")
    LISTAT["pisteet"] = []
    if not ELEMENTIT["tallennusnappi"]:
        ELEMENTIT["tallennusnappi"] = ikkunasto.luo_nappi(
            ELEMENTIT["vasen_yla_kehys"], "Tallenna...", tallenna_kuvaaja
        )
    if not ELEMENTIT["poistonappi"]:
        ELEMENTIT["poistonappi"] = ikkunasto.luo_nappi(
            ELEMENTIT["vasen_yla_kehys"], "Poista tausta", poista_tausta
        )

def tyhjaa_muisti():
    """
    Napinkäsittelijä, joka tyhjentää ohjelman muistissa olevan datan
    ja palauttaa ohjelman alkutilaan.
    Tämän tekeminen erillisellä napilla mahdollistaa useamman datakansion käsittelyn yhtä aikaa.
    """
    
    LISTAT["energiat"] = []
    LISTAT["intensiteetit"] = []
    LISTAT["ladatut"] = 0
    LISTAT["piikkien_I"] = []
    LISTAT["pisteet"] = []
    LISTAT["virheelliset"] = []
    for avain in ELEMENTIT:
        if avain.endswith("nappi"):
            try:
                ikkunasto.poista_elementti(ELEMENTIT[avain])
            except AttributeError:
                pass
            else:
                ELEMENTIT[avain] = False
    ELEMENTIT["akselit"].cla()
    ELEMENTIT["akselit"].grid(True)
    ELEMENTIT["piirtoalue"].draw()
    ikkunasto.paivita_tekstirivi(ELEMENTIT["tekstirivi"], "")
    ikkunasto.kirjoita_tekstilaatikkoon(ELEMENTIT["tekstilaatikko"], "Muisti tyhjennetty.", True)

def luo_taulukot(energiat, intensiteetit, arvot):
    """
    Luo ohjelman muistiin kaksi taulukkoa,
    joista toisessa on mitatut kineettiset energiat ja
    toisessa summa jokaisesta mitatusta intensiteettispektristä energiaa kohden.
    Palautus on toteutettu yhtenä palautettavana listana funktiokutsun pituuden vuoksi.
    
    :param list energiat: lista, joka sisältää mitatut energiat
    :param list intensiteetit: lista, joka sisältää mitatut intensiteetit
    :param tuple arvot: monikko, jonka ensimmäinen arvo on lisättävä energia, toinen intensiteetti
    :return: lista, joka sisältää päivitetyt listat energioista ja intensiteeteistä
    """
    
    uudet = []
    for i, E in enumerate(energiat):
        if E == arvot[0]:
            intensiteetit[i] = intensiteetit[i] + arvot[1]
            uudet.append(energiat)
            uudet.append(intensiteetit)
            return uudet
    else:
        energiat.append(arvot[0])
        intensiteetit.append(arvot[1])
        uudet.append(energiat)
        uudet.append(intensiteetit)
        return uudet

def lue_data(kansio):
    """
    Lukee kaikki datatiedostot annetusta kansiosta.
    Ohittaa tiedostot, jotka eivät ole muotoa measurement_x.txt sekä tiedostot,
    joiden sisältämässä datassa on virheitä.
    
    Funktio päivittää globaalin sanakirjan, joka kokoaa kaiken tarpeellisen datan.
    Se sisältää kolme listaa sekä onnistuneesti ladattujen tiedostojen lukumäärän.
    Energiat-lista sisältää sidosenergiat (yksikkönä elektronivoltti).
    Näiden pitäisi olla samat eri mittausten välillä, joten listaa päivitetään vain,
    jos lisättävää arvoa ei listaa läpikäydessä kohdata.
    Intensiteetit-lista sisältää jokaista energiatasoa kohden summan sen mitatuista intensiteeteistä.
    Virheelliset-lista kokoaa listan hylättyjen tiedostojen nimiä.
    Välilista on ainoastaan funktion sisäisessä käytössä oleva lista,
    johon kerätään kelvollisia datarivejä lopullisia datalistoja varten,
    mutta se tyhjätään ja tiedosto hylätään heti, jos virheitä kohdataan.
    
    Yritin funktion jakamista vielä useampaan funktioon, mutta tämä on ehdottomasti
    mutkattomin, ongelmattomin ja loppujen lopuksi selkein ratkaisu, minkä keksin.
    
    :param str kansio: polku datatiedostojen kansioon
    """
    
    valilista = []
    LISTAT["ladatut"] = 0
    LISTAT["virheelliset"] = []
    
    sisalto = os.listdir(kansio)
    for tiedosto in sisalto:
        polku = os.path.join(kansio, tiedosto)
        if os.path.isfile(polku):
            nimijako = tiedosto.rsplit(".", 1)
            if nimijako[0].startswith("measurement_") and nimijako[1] == "txt":
                with open(polku) as lahde:
                    for rivi in lahde.readlines():
                        data = rivi.split()
                        if len(data) == 2:
                            try:
                                data[0] = float(data[0])
                                data[1] = float(data[1])
                            except ValueError:
                                LISTAT["virheelliset"].append(tiedosto)
                                valilista = []
                                break
                            else:
                                data = tuple(data)
                                valilista.append(data)
                        else:
                            LISTAT["virheelliset"].append(tiedosto)
                            valilista = []
                            break
                    else:
                        for arvot in valilista:
                            uudet = luo_taulukot(LISTAT["energiat"], LISTAT["intensiteetit"], arvot)
                            LISTAT["energiat"] = uudet[0]
                            LISTAT["intensiteetit"] = uudet[1]
                        LISTAT["ladatut"] += 1
                        valilista = []

def avaa_kansio():
    """
    Napinkäsittelijä, joka pyytää käyttäjää valitsemaan kansion avaamalla kansioselaimen.
    Lataa datan valitusta kansiosta ja syöttää sen lue_data-funktiolle käsittelyyn.
    Tulostaa sitten tekstilaatikkoon listan virheellisistä tiedostoista ja
    ilmoittaa montako tiedostoa ladattiin onnistuneesti.
    Kutsuu lopuksi piirra_data-funktiota kuvaajan piirtämiseksi.
    Mikäli annetussa kansiossa ei ollut yhtään dataa, ilmoitetaan tästä käyttäjälle.
    """
    
    kohdekansio = ikkunasto.avaa_hakemistoikkuna("Valitse datakansio...")
    if kohdekansio:
        avausilmoitus = "Luetaan {} sisältö...".format(kohdekansio)
        ikkunasto.kirjoita_tekstilaatikkoon(ELEMENTIT["tekstilaatikko"], avausilmoitus)
        lue_data(kohdekansio)
        ikkunasto.kirjoita_tekstilaatikkoon(ELEMENTIT["tekstilaatikko"], "Sisältö luettu.")
        for i in LISTAT["virheelliset"]:
            ikkunasto.kirjoita_tekstilaatikkoon(ELEMENTIT["tekstilaatikko"], "Viallinen tiedosto: " + i)
        latausilmoitus = "Ladattiin {} tiedostoa.".format(LISTAT["ladatut"])
        ikkunasto.kirjoita_tekstilaatikkoon(ELEMENTIT["tekstilaatikko"], latausilmoitus)
        ei_dataa_viesti = "Kohdekansiosta ei löytynyt yhtään kelvollista dataa."
        if len(LISTAT["energiat"]) < 1 or len(LISTAT["intensiteetit"]) < 1:
            ikkunasto.avaa_viesti_ikkuna("Kelvollista dataa ei löytynyt", ei_dataa_viesti, True)
        else:
            piirra_data()

def main():
    """
    Luo käyttöliittymäikkunan,
    jossa vasemmalla on kolme nappia,
    joista kaksi alinta on erotettu vaakaerottimella,
    oikealla taas on kuvaaja, tekstirivi sekä tekstilaatikko.
    Käyttöliittymä koostuu yhteensä neljästä kehyksestä;
    vasen "emo" kehys ja oikea kehys jakavat ikkunan kahteen osaan.
    Vasen kehys taas jaetaan pystysuunnassa vielä kahteen osaan,
    mikä mahdollistaa nappien lisäämisen ohjelman edetessä ilman,
    että vaakaerottimen alle tulevat lopetus- ja tyhjennysnapit
    menevät muiden kanssa sekaisin.
    """
    
    ikkuna = ikkunasto.luo_ikkuna("Spektrimestari v.{}".format(VERSIO)) 
    vasen_emo_kehys = ikkunasto.luo_kehys(ikkuna)
    ELEMENTIT["vasen_yla_kehys"] = ikkunasto.luo_kehys(vasen_emo_kehys, ikkunasto.YLA)
    vasen_ala_kehys = ikkunasto.luo_kehys(vasen_emo_kehys, ikkunasto.YLA)
    oikea_kehys = ikkunasto.luo_kehys(ikkuna)
    ikkunasto.luo_nappi(ELEMENTIT["vasen_yla_kehys"], "Avaa...", avaa_kansio)
    ikkunasto.luo_vaakaerotin(vasen_ala_kehys)
    ikkunasto.luo_nappi(vasen_ala_kehys, "Ohje", nayta_ohje)
    ikkunasto.luo_nappi(vasen_ala_kehys, "Tyhjennä", tyhjaa_muisti)
    ikkunasto.luo_nappi(vasen_ala_kehys, "Lopeta", ikkunasto.lopeta)
    piirtoalue, kuvaaja = ikkunasto.luo_kuvaaja(oikea_kehys, valitse_datapiste, 600, 400)
    akselit = kuvaaja.subplots()
    kuvaaja.suptitle("Spektri")
    akselit.grid(True)
    ELEMENTIT["piirtoalue"] = piirtoalue
    ELEMENTIT["kuvaaja"] = kuvaaja
    ELEMENTIT["akselit"] = akselit
    ELEMENTIT["tekstirivi"] = ikkunasto.luo_tekstirivi(oikea_kehys, "")
    ELEMENTIT["tekstilaatikko"] = ikkunasto.luo_tekstilaatikko(oikea_kehys, 60, 20)
    ikkunasto.kaynnista()

if __name__ == "__main__":
    main()

