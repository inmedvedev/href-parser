from href_parser.celery import app
from .models import DomainInfo, Address, TxtRecord, NameServer, MailExchange
import requests
import time


@app.task
def load_domain_data(urls, base_url):
    if bool(DomainInfo.objects.filter(base_url=base_url)):
        load_domain_data.update_state(state='SUCCESS')
    for url in urls:
        api_url = f'https://api.domainsdb.info/v1/domains/search?domain={url}'
        response = requests.get(api_url)
        response.raise_for_status()
        time.sleep(0.1)
        raw_data = response.json()

        domains_info = [
            DomainInfo(
                base_url=base_url,
                url=url,
                domain=domain['domain'],
                create_date=domain['create_date'],
                update_date=domain['update_date'],
                country=domain['country'],
                is_dead=domain['isDead']
            )
            for domain in raw_data['domains']
        ]
        domain_info_objects = DomainInfo.objects.bulk_create(domains_info)
        all_address_info = []
        for domain_object, extra_data in zip(domain_info_objects, raw_data['domains']):
            if extra_data['A'] is None:
                all_address_info.append(Address(
                    url=domain_object,
                    ip=None
                ))
            else:
                all_address_info += [
                    Address(
                        url=domain_object,
                        ip=ip
                    ) for ip in extra_data['A']
                ]
        Address.objects.bulk_create(all_address_info)


