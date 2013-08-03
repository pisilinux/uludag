/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef KAPTAN_H
#define KAPTAN_H

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <kwizard.h>

class KLocale;

class Welcome;
class MouseSetup;
class Wallpaper;
class Goodbye;

class Kaptan : public KWizard
{
    Q_OBJECT

public:
    Kaptan( QWidget* parent=0, const char *name=0 );
    ~Kaptan();

    virtual void next();
    virtual void back();

public slots:
    virtual void accept();
    virtual void reject();

private:
    KLocale *locale;
    Welcome *welcome;
    MouseSetup *mouse;
    Wallpaper *wallpaper;
    Goodbye *goodbye;

protected:
    virtual void closeEvent(QCloseEvent*);
};

#endif // KAPTAN_H
