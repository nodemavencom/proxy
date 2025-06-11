# 📘 NodeMaven Proxy Ruleset Reference

This document outlines all possible combinations for generating proxies using NodeMaven’s dashboard. It includes configuration rules, example strings, and construction logic.

---

## 🔧 Base Proxy Format

{host}:{port}:{username}:{password}


- `host`: `gate.nodemaven.com`
- `port`: `1080` for SOCKS5 or `8080` for HTTP
- `username`: Encodes all proxy settings (location, session, etc.)
- `password`: Shown in dashboard (usually same as username prefix)

---

## 1️⃣ Connection Types

| Type        | Tag in Username         | Example Segment                     |
|-------------|--------------------------|-------------------------------------|
| Residential | *(default / optional)*   | `...country-any...`                 |
| Mobile      | `type-mobile`            | `...type-mobile...`                 |

---

## 2️⃣ IP Version

| Option       | Tag         | Notes                |
|--------------|-------------|----------------------|
| IPv4 + IPv6  | *(default)* | Tag omitted          |
| IPv4 only    | `ipv4-true` | Explicit IPv4 use    |

✅ Example:

...type-mobile-ipv4-true...

---

## 3️⃣ Location Settings

| Level   | Format                        | Example Tag                            |
|---------|-------------------------------|----------------------------------------|
| Country | `country-xx`                 | `country-us`                           |
| Region  | `region-region_name`         | `region-new_york`                      |
| City    | `city-city_name`             | `city-brooklyn`                        |
| ISP     | `isp-isp_name`               | `isp-beeline_home`                     |

✅ Example:

...country-us-region-new_york-city-brooklyn...


---

## 4️⃣ Session Type

| Type              | Tag Example                                 | Notes                                  |
|-------------------|---------------------------------------------|----------------------------------------|
| Rotating (default)| *(no sid, ttl)*                             | Changes each request                   |
| Sticky            | `sid-{session}`                             | Static IP until session expires        |
| Sticky + TTL      | `sid-{session}-ttl-{duration}`              | TTL: `60s`, `1m`, `5m`, `24h`, etc.     |

✅ Examples:

...sid-a49c071423294...
...sid-a49c071423294-ttl-1m...
...sid-a49c071423294-ttl-24h...

---

## 5️⃣ IP Quality Filter

| Option         | Tag             | Notes                              |
|----------------|------------------|-------------------------------------|
| No filter      | *(omit tag)*     | All IPs                            |
| Medium filter  | `filter-medium`  | Higher trust IPs                   |

✅ Examples:

...filter-medium...

yaml

---

## 6️⃣ Protocol & Port

| Protocol | Port  | Use Case          |
|----------|-------|-------------------|
| HTTP     | 8080  | Browser/manual     |
| SOCKS5   | 1080  | Scripts & scraping |

---

## ✅ Combined Proxy Examples

### Mobile / IPv4 / Sticky / TTL / Filter
gate.nodemaven.com:1080:aa101d91571b74-country-any-type-mobile-ipv4-true-sid-a49c071423294-ttl-24h-filter-medium:a101d91571b74

### Residential / US / Brooklyn / Rotating / No Filter
gate.nodemaven.com:1080:aa101d91571b74-country-us-region-new_york-city-brooklyn:a101d91571b74

### Mobile / Russia / Sticky 60s / ISP / Filter
gate.nodemaven.com:1080:aa101d91571b74-country-ru-region-moscow-city-moscow-isp-beeline_home-type-mobile-ipv4-true-sid-a49c071423294-ttl-1m-filter-medium:a101d91571b74

---

## 🧩 Optional Rule Builder

| Section         | Required? | Value Source             |
|----------------|-----------|---------------------------|
| `country-*`     | ✅ Yes    | Manual or dropdown        |
| `region-*`      | Optional  | Manual                    |
| `city-*`        | Optional  | Manual                    |
| `isp-*`         | Optional  | Manual                    |
| `type-mobile`   | If mobile | Dropdown                  |
| `ipv4-true`     | If chosen | IP version toggle         |
| `sid-*`         | Optional  | Session type field        |
| `ttl-*`         | Optional  | Sticky + custom duration  |
| `filter-medium` | Optional  | Quality filter toggle     |

---

> ✅ Keep this reference handy for building any custom NodeMaven proxy configuration string manually or validating large batches.