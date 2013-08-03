/*
  Copyright (c) 2004, TUBITAK/UEKAE

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  Please read the COPYING file.
*/

#ifndef WALLPAPER_H
#define WALLPAPER_H

#include "wallpaperdlg.h"

class KStandardDirs;
class QString;

class Wallpaper : public WallpaperDlg
{
    Q_OBJECT

public:
    Wallpaper( QWidget *parent = 0, const char* name = 0 );
    bool changeWallpaper();
    void setWallpaper();

protected slots:
    void paperSelected( int );
    void checkChanged( bool change );

private:
    KStandardDirs *mDirs;
    QMap<QString, int> papers;
    QString selectedPaper;
    bool changePaper;
};

#endif // WELCOME_H
