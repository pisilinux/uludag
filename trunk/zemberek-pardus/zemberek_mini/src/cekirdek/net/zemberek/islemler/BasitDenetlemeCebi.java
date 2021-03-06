package net.zemberek.islemler;

import net.zemberek.bilgi.KaynakYukleyici;

import java.util.HashSet;
import java.util.Set;
import java.io.BufferedReader;
import java.io.IOException;

/**
 * User: ahmet
 * Date: Jun 12, 2006
 */
public class BasitDenetlemeCebi implements DenetlemeCebi {

    private final Set<String> cep;

    public BasitDenetlemeCebi(String dosyaAdi) throws IOException {
        BufferedReader rd = new KaynakYukleyici("UTF-8").getReader(dosyaAdi);
        cep = new HashSet<String>(2500);
        while (rd.ready()) {
            ekle(rd.readLine());
        }
        rd.close();
    }

    public boolean kontrol(String str) {
        return cep.contains(str);
    }

    public synchronized void ekle(String s) {
        cep.add(s);
    }

    public synchronized void sil(String s) {
        cep.remove(s);
    }
}
