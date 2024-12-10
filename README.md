# MEXC Trading Terminal

Bu Python scripti, MEXC borsasında spot trade yapmanızı sağlayacak bir terminal uygulamasıdır. USDT bakiyenizi sorgulayıp, belirli bir miktarda veya tüm bakiyenizi alıp satabilirsiniz.

## Özellikler
- **USDT Bakiyesini Sorgulama**: Mevcut USDT bakiyenizi sorgulayıp terminalde görüntüleyebilirsiniz.
- **Piyasa Emirleri (Market Orders)**: 
  - Örneğin terminale yazacağınız `btc 100 buy` komutuyla uygulamaya girip işlem yapmak istediğiniz pariteyi bulup alış girmek yerine hızlı bir şekilde komutla 100 USD değerinde BİTCOİN aldık ya da belirttiğiniz miktarda USD karşılığında alım yapabilirsiniz.
  - `btc sell` komutuyla belirttiğiniz semboldeki tüm bakiyenizi satabilirsiniz.
- **Sembol Doğrulaması**: İşlem yapmadan önce girilen sembolün geçerli olup olmadığı kontrol edilir.

## Kullanım

### Gereksinimler
- Python 3.x
- `requests` kütüphanesi: Bu script, API'ye istek yapmak için `requests` kütüphanesini kullanır. Yüklemek için şu komutu çalıştırabilirsiniz:
  
  ```bash
  pip install requests
