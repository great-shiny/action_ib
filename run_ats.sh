#!/bin/bash

# bash ~/z_mac/ws_python/ats_prod/run_ats.sh DEV 68112231
# bash ~/z_mac/ws_python/ats_prod/run_ats.sh DEV 64552937
ENV=$1
account=$2  # 첫 번째 인자를 account로 사용

if [ "$ENV" == 'DEV' ]; then
 source /opt/anaconda3/etc/profile.d/conda.sh
 conda activate ats_prod_py39
 cd ~/z_mac/github/action_ib
fi

# account 값에 따라 APP_KEY를 설정합니다.
case "$account" in
  "68112231")
    APP_KEY="PSzAvVIRO5cD4ZDcUzNFDRImXujEozBYdJRN"
    APP_SECRET="GxymCb1dDHrZS9BGvDHVnReh78jgCnSZ7lcCa5lDzkM3cubjDSFnjFHHXQCxqmd8vAnYS85Ge3SI1udnz/MpEm/ma0wIoAeffC40GpEIO8oqRASysPpbrqmB/860xB7HHjFG0kQ+NbmWs7PWF+UnOHPKd6Fx4KaP6WsmsIwpYfrnHXGgTlI="
    DEPOSIT=27345
    PARTITIONS=40
    THRESHOLD=12
    TICKER="NAIL"
    ;;
  "64552937")
    APP_KEY="PShrvK31z3VWxzrkQbry7IVHEgP8q4u3Z5Z0"
    APP_SECRET="+7//EFp//RglChM7Mknkdk9TI9eJqURybgjQ1EPHRyoxCvVyd8+RahjiHYJiCDVNgjvSNuC714jdDC/TjbUfdbWshi8ajq7kri1gWWhugEZ4MOMGTqNn6UfBtwJ+Ijg+EszGXJ7/8gpTZKqIukVvC9XPXVv6ALmv59EfszjVN7MFeoTfo88="
    DEPOSIT=23087
    PARTITIONS=40
    THRESHOLD=12
    TICKER="SOXL"
    ;;
  *)
    echo "Invalid account. Please specify a valid account."
    exit 1
    ;;
esac

python3 main.py --env "$ENV" --account "$account" --appkey $APP_KEY --appsecret $APP_SECRET --deposit $DEPOSIT --partitions $PARTITIONS --threshold $THRESHOLD --ticker $TICKER

if [ "$ENV" == 'DEV' ]; then
 conda deactivate
fi
