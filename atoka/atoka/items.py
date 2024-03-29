# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AtokaContactsItem(scrapy.Item):
    code = scrapy.item.Field(serializer=str)
    company_name = scrapy.item.Field(serializer=str)
    url = scrapy.item.Field(serializer=str)
    vat_id = scrapy.item.Field(serializer=str)
    numero_rea = scrapy.item.Field(serializer=str)
    emails = scrapy.item.Field()
    phones = scrapy.item.Field()
    faxes = scrapy.item.Field()
    websites = scrapy.item.Field()
    wikipedia = scrapy.item.Field(serializer=str)
    social = scrapy.item.Field()

    def __add__(self, other):
        data_field_mapping = {
            'emails': 'address',
            'phones': 'number',
            'websites': 'url',
            'faxes': None,
            'social': 'url',
        }
        if isinstance(other, self.__class__):
            for field in self.fields:
                if other[field]:
                    if isinstance(self[field], str):
                        if other[field] not in self[field]:
                            self[field] = self[field] + ' (O) ' + other[field]
                    elif isinstance(self[field], list):
                        self._add_list_items(other[field], field, data_field_mapping[field])
                    elif isinstance(self[field], dict):
                        self._add_dict_items(other[field], field, data_field_mapping[field])
        return self

    def _add_list_items(self, objects, main_field, field=None):
        for obj in objects:
            if field is not None:
                obj[field] = '(O) ' + obj[field] if obj.get(field) else ''
                if obj[field]:
                    self[main_field].append(obj)
            else:
                self[main_field].append(''.join(['(O) ', obj]))

    def _add_dict_items(self, objects, main_field, field):
        for key, value in objects.items():
            if value and isinstance(value, list):
                for obj in value:
                    obj[field] = '(O) ' + obj[field] if obj.get(field) else ''
                    if obj[field]:
                        if self[main_field].get(key) is None:
                            self[main_field][key] = []
                        self[main_field][key].append(obj)


class AtokaPersonsInfoItem(scrapy.Item):
    code = scrapy.item.Field(serializer=str)
    people = scrapy.item.Field()

    def __add__(self, other):
        field = 'people'
        full_name_field = 'fullName'
        list_of_people_full_names = [obj.get(full_name_field) for obj in self[field]]
        for item in other.get(field):
            person_full_name = item.get(full_name_field)
            if person_full_name not in list_of_people_full_names:
                item[full_name_field] = '(O) ' + person_full_name
                self[field].append(item)
        return self


class AtokaErrorContactsItem(scrapy.Item):
    code = scrapy.item.Field(serializer=str)
    reason = scrapy.item.Field(serializer=str)
