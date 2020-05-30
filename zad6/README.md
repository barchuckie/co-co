# ZAD 6

Pliki zawierające rozwiązanie listy 6:
  - ```compressor.py``` - program kodujący
  - ```decompressor.py``` - program dekodujący
  - ```compare.py``` - program porównujący pliki
  - ```bands.py``` - implementacja filtrów (pasm) górnoprzepustowego i dolnoprzepustowego
  - ```decoding.py``` - dekodowanie pasm
  - ```differential_coding.py``` - kodowanie różnicowe
  - ```distortion.py``` - obliczanie MSE oraz SNR
  - ```encoding.py``` - kodowanie pasm
  - ```inout_bits.py``` - czytanie i zapisywanie bitów
  - ```pixels.py``` - implementacja pikseli i ich zbiorów
  - ```quantization.py``` - kwantyzacja nierównomierna
  - ```tga.py``` - czytanie i tworzenie plików TGA

#### Uruchomienie programu kodującego:

```python3 compressor.py input_file output_file quantizer_bits```

gdzie:
  - ```input_file``` - plik wejściowy do skompresowania (TGA)
  - ```output_file``` - skompresowany plik wynikowy (bin)
  - ```quantizer_bits``` - liczba bitów kwantyzatora


#### Uruchomienie programu dekodującego:

```python3 decompressor.py input_file output_file```

gdzie:
  - ```input_file``` - skompresowany plik wejściowy do zdekodowania (bin)
  - ```output_file``` - zdekompresowany plik wynikowy (TGA)


#### Uruchomienie programu porównującego:

```python3 compare.py original reconstructed```

gdzie:
  - ```original``` - Oryginalny plik TGA
  - ```reconstructed``` - Plik TGA po odkodowaniu

