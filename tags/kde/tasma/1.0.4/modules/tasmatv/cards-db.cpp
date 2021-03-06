/*
  Copyright (c) 2006, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#include <qlistbox.h>
#include <qstringlist.h>
#include <klocale.h>
#include <kdebug.h>

extern "C" {
#include "pci.h"
}

#include "cards-db.h"

#define NOF_CARDS 137

/* bt8x8 chipset cards */
static struct BTTV_CARD {
  unsigned int vendor_id;
  unsigned int card_id;
  const char *card_name;
} bttv_cards[NOF_CARDS] = {
  { 0xffff, 0, "Otomatik" },
  { 0x11bd, 1, "MIRO PCTV" },
  { 0x0070, 2, "Hauppauge (bt848)" },
  { 0x10b4, 3, "STB, Gateway P/N 6000699 (bt848)"},
  { 0x8086, 4, "Intel Create and Share PCI/ Smart Video Recorder III"},
  { 0x1092, 5, "Diamond DTV2000"},
  { 0x1461, 6, "AVerMedia TVPhone"},
  { 0xffff, 7, "MATRIX-Vision MV-Delta"},
  { 0x5168, 8, "Lifeview FlyVideo II (Bt848) LR26 / MAXI TV Video PCI2 LR26"},
  { 0xffff, 9, "IMS/IXmicro TurboTV"},
  { 0x0070, 10, "Hauppauge (bt878)"},
  { 0x11bd, 11, "MIRO PCTV pro"},
  { 0x1421, 12, "ADS Technologies Channel Surfer TV (bt848)"},
  { 0x1461, 13, "AVerMedia TVCapture 98"},
  { 0x12cd, 14, "Aimslab Video Highway Xtreme (VHX)"},
  { 0x15b0, 15, "Zoltrix TV-Max"},
  { 0x1554, 16, "Prolink Pixelview PlayTV (bt878)"},
  { 0x107d, 17, "Leadtek WinView 601"},
  { 0xffff, 18, "AVEC Intercapture"},
  { 0x5168, 19, "Lifeview FlyVideo II EZ /FlyKit LR38 Bt848 (capture only)"},
  { 0xffff, 20, "CEI Raffles Card"},
  { 0x5168, 21, "Lifeview FlyVideo 98/ Lucky Star Image World ConferenceTV LR50"},
  { 0xffff, 22, "Askey CPH050/ Phoebe Tv Master + FM"},
  { 0xffff, 23, "Modular Technology MM201/MM202/MM205/MM210/MM215 PCTV, bt878"},
  { 0xffff, 24, "Askey CPH05X/06X (bt878) [many vendors]"},
  { 0x153b, 25, "Terratec TerraTV+ Version 1.0 (Bt848)/ Terra TValue Version 1.0/ Vobis TV-Boostar"},
  { 0x0070, 26, "Hauppauge WinCam newer (bt878)"},
  { 0x5168, 27, "Lifeview FlyVideo 98/ MAXI TV Video PCI2 LR50"},
  { 0x153b, 28, "Terratec TerraTV+ Version 1.1 (bt878)"},
  { 0x1295, 29, "Imagenation PXC200"},
  { 0x5168, 30, "Lifeview FlyVideo 98 LR50"},
  { 0xffff, 31, "Formac iProTV, Formac ProTV I (bt848)"},
  { 0x8086, 32, "Intel Create and Share PCI/ Smart Video Recorder III"},
  { 0x153b, 33, "Terratec TerraTValue Version Bt878"},
  { 0x107d, 34, "Leadtek WinFast 2000/ WinFast 2000 XP"},
  { 0x5168, 35, "Lifeview FlyVideo 98 LR50 / Chronos Video Shuttle II"},
  { 0x5168, 36, "Lifeview FlyVideo 98FM LR50 / Typhoon TView TV/FM Tuner"},
  { 0x1554, 37, "Prolink PixelView PlayTV pro"},
  { 0xffff, 38, "Askey CPH06X TView99"},
  { 0x11bd, 39, "Pinnacle PCTV Studio/Rave"},
  { 0xffff, 40, "STB TV PCI FM, Gateway P/N 6000704 (bt878), 3Dfx VoodooTV 100"},
  { 0x1461, 41, "AVerMedia TVPhone 98"},
  { 0xffff, 42, "ProVideo PV951"},
  { 0xffff, 43, "Little OnAir TV"},
  { 0xffff, 44, "Sigma TVII-FM"},
  { 0xffff, 45, "MATRIX-Vision MV-Delta 2"},
  { 0x15b0, 46, "Zoltrix Genie TV/FM"},
  { 0x153b, 47, "Terratec TV/Radio+"},
  { 0xffff, 48, "Askey CPH03x/ Dynalink Magic TView"},
  { 0xffff, 49, "IODATA GV-BCTV3/PCI"},
  { 0x1554, 50, "Prolink PV-BT878P+4E / PixelView PlayTV PAK / Lenco MXTV-9578 CP"},
  { 0xffff, 51, "Eagle Wireless Capricorn2 (bt878A)"},
  { 0x11bd, 52, "Pinnacle PCTV Studio Pro"},
  { 0xffff, 53, "Typhoon TView RDS + FM Stereo / KNC1 TV Station RDS"},
  { 0x5168, 54, "Lifeview FlyVideo 2000 /FlyVideo A2/ Lifetec LT 9415 TV [LR90]"},
  { 0xffff, 55, "Askey CPH031/ BESTBUY Easy TV"},
  { 0x5168, 56, "Lifeview FlyVideo 98FM LR50"},
  { 0xffff, 57, "GrandTec 'Grand Video Capture' (Bt848)"},
  { 0xffff, 58, "Askey CPH060/ Phoebe TV Master Only (No FM)"},
  { 0xffff, 59, "Askey CPH03x TV Capturer"},
  { 0xffff, 60, "Modular Technology MM100PCTV"},
  { 0xffff, 61, "AG Electronics GMV1"},
  { 0xffff, 62, "Askey CPH061/ BESTBUY Easy TV (bt878)"},
  { 0x1002, 63, "ATI TV-Wonder"},
  { 0x1002, 64, "ATI TV-Wonder VE"},
  { 0x5168, 65, "Lifeview FlyVideo 2000S LR90"},
  { 0x153b, 66, "Terratec TValueRadio"},
  { 0xffff, 67, "IODATA GV-BCTV4/PCI"},
  { 0x121a, 68, "3Dfx VoodooTV FM (Euro), VoodooTV 200 (USA)"},
  { 0xffff, 69, "Active Imaging AIMMS"},
  { 0x1554, 70, "Prolink Pixelview PV-BT878P+ (Rev.4C,8E)"},
  { 0x5168, 71, "Lifeview FlyVideo 98EZ (capture only) LR51"},
  { 0x1554, 72, "Prolink Pixelview PV-BT878P+9B (PlayTV Pro rev.9B FM+NICAM)"},
  { 0xffff, 73, "Sensoray 311"},
  { 0xffff, 74, "RemoteVision MX (RV605)"},
  { 0xffff, 75, "Powercolor MTV878/ MTV878R/ MTV878F"},
  { 0xffff, 76, "Canopus WinDVR PCI (COMPAQ Presario 3524JP, 5112JP)"},
  { 0xffff, 77, "GrandTec Multi Capture Card (Bt878)"},
  { 0xffff, 78, "Jetway TV/Capture JW-TV878-FBK, Kworld KW-TV878RF"},
  { 0xffff, 79, "DSP Design TCVIDEO"},
  { 0x0070, 80, "Hauppauge WinTV PVR"},
  { 0xffff, 81, "IODATA GV-BCTV5/PCI"},
  { 0x1576, 82, "Osprey 100/150 (878)"},
  { 0x1576, 83, "Osprey 100/150 (848)"},
  { 0x1576, 84, "Osprey 101 (848)"},
  { 0x1576, 85, "Osprey 101/151"},
  { 0x1576, 86, "Osprey 101/151 w/ svid"},
  { 0x1576, 87, "Osprey 200/201/250/251"},
  { 0x1576, 88, "Osprey 200/250"},
  { 0x1576, 89, "Osprey 210/220"},
  { 0x1576, 90, "Osprey 500"},
  { 0x1576, 91, "Osprey 540"},
  { 0x1576, 92, "Osprey 2000"},
  { 0xffff, 93, "IDS Eagle"},
  { 0x11bd, 94, "Pinnacle PCTV Sat"},
  { 0xffff, 95, "Formac ProTV II (bt878)"},
  { 0xffff, 96, "MachTV"},
  { 0xffff, 97, "Euresys Picolo"},
  { 0xffff, 98, "ProVideo PV150"},
  { 0xffff, 99, "AD-TVK503"},
  { 0xffff, 100, "Hercules Smart TV Stereo"},
  { 0xffff, 101, "Pace TV & Radio Card"},
  { 0xffff, 102, "IVC-200"},
  { 0xffff, 103, "Grand X-Guard / Trust 814PCI"},
  { 0xffff, 104, "Nebula Electronics DigiTV"},
  { 0xffff, 105, "ProVideo PV143"},
  { 0xffff, 106, "PHYTEC VD-009-X1 MiniDIN (bt878)"},
  { 0xffff, 107, "PHYTEC VD-009-X1 Combi (bt878)"},
  { 0xffff, 108, "PHYTEC VD-009 MiniDIN (bt878)"},
  { 0xffff, 109, "PHYTEC VD-009 Combi (bt878)"},
  { 0xffff, 110, "IVC-100"},
  { 0xffff, 111, "IVC-120G"},
  { 0xffff, 112, "pcHDTV HD-2000 TV"},
  { 0xffff, 113, "Twinhan DST + clones"},
  { 0xffff, 114, "Winfast VC100"},
  { 0xffff, 115, "Teppro TEV-560/InterVision IV-560"},
  { 0xffff, 116, "SIMUS GVC1100"},
  { 0xffff, 117, "NGS NGSTV+"},
  { 0xffff, 118, "LMLBT4"},
  { 0xffff, 119, "Tekram M205 PRO"},
  { 0xffff, 120, "Conceptronic CONTVFMi"},
  { 0xffff, 121, "Euresys Picolo Tetra"},
  { 0xffff, 122, "Spirit TV Tuner"},
  { 0x1461, 123, "AVerMedia AVerTV DVB-T 771"},
  { 0x1461, 124, "AverMedia AverTV DVB-T 761"},
  { 0xffff, 125, "MATRIX Vision Sigma-SQ"},
  { 0xffff, 126, "MATRIX Vision Sigma-SLC"},
  { 0xffff, 127, "APAC Viewcomp 878(AMAX)"},
  { 0xffff, 128, "DViCO FusionHDTV DVB-T Lite"},
  { 0xffff, 129, "V-Gear MyVCD"},
  { 0xffff, 130, "Super TV Tuner"},
  { 0xffff, 131, "Tibet Systems 'Progress DVR' CS16"},
  { 0xffff, 132, "Kodicom 4400R (master)"},
  { 0xffff, 133, "Kodicom 4400R (slave)"},
  { 0xffff, 134, "Adlink RTV24"},
  { 0xffff, 135, "DViCO FusionHDTV 5 Lite"},
  { 0xffff, 136, "Acorp Y878F"}
};

CardsDB::CardsDB()
{
    initVendors();
}

CardsDB::~CardsDB()
{
    CardVendors::Iterator it;
    for (it = m_vendors.begin(); it != m_vendors.end(); ++it) {
	delete(it.data());
    }
}

void CardsDB::getCards(QString vendor, QStringList *cards)
{
    Cards::ConstIterator it;

    for (it = m_vendors[vendor]->begin(); it != m_vendors[vendor]->end(); it++) {
	cards->append(it->card_name);
    }
}

void CardsDB::getVendors(QStringList *vendors)
{
    CardVendors::ConstIterator it;

    for (it = m_vendors.begin(); it != m_vendors.end(); ++it) {
	vendors->append(it.key());
    }
}

int CardsDB::getCard(QString card_name)
{
    for (unsigned int i = 0; i < sizeof(bttv_cards); i++) {
	if (card_name == bttv_cards[i].card_name)
	    return bttv_cards[i].card_id;
    }

    return -1;
}

int CardsDB::getCard(unsigned int card_id, QString &vendor_name, QString &card_name)
{
    CardVendors::ConstIterator v_it;
    Cards::ConstIterator c_it;

    for (v_it = m_vendors.begin(); v_it != m_vendors.end(); ++v_it) {
	for (c_it = v_it.data()->begin(); c_it != v_it.data()->end(); ++c_it) {
	    if (c_it->card_id == card_id) {
		vendor_name = v_it.key();
		card_name = c_it->card_name;
		return card_id;
	    }
	}
    }

    return -1;
}

void CardsDB::initVendors()
{
    Cards *cards;
    struct Card card;
    struct pci_access *pacc;
    char devbuf[128];

    pacc = pci_alloc();

    for (int i = 0; i < NOF_CARDS; i++) {

	QString vendor = (bttv_cards[i].vendor_id == 0xffff ? i18n("Other") : 
			  pci_lookup_name(pacc, devbuf, sizeof(devbuf), PCI_LOOKUP_VENDOR, bttv_cards[i].vendor_id, 0));

	card.card_id = bttv_cards[i].card_id;
	card.card_name = bttv_cards[i].card_name;

	if (!m_vendors.contains(vendor)) {
	    cards = new Cards();
	    m_vendors[vendor] = cards;
	} else {
	    cards = m_vendors[vendor];
	}

	cards->push_back(card);
    }

    pci_cleanup(pacc);
}

