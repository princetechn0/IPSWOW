# IPSWOW

I built this tool to help save time. Many customers do not have computers to erase their phones, so I would do it for them, yet it was always an extra wait time of about 15 minutes to download the right IPSW.

Therefore, I wanted a tool to allow for bulk IPSW downloading of the latest firmwares.

This tool is great for developers, repair shops, and schools!


# Change Log

## 2022-05-20

### Changed
- Resolved Postgres DB issues on Heroku. 
- Better handling of exceptions. 
- Heroku crashes resolved. Site is running. 

## 2022-05-19
- Site currently experiencing issues due to database problems. Going up and down periodically. Will fix in near future. Sorry for inconvenience. 

## 2022-05-11

### Changed
- Transitioned to relational database for storing IPSW information.
  - Improves load times
  - Reduces data usage
- Cleaned code. 

### Issues
- Previously saved presets will be out of format. Please delete and create again. 
- Presets not updating to use latest IPSW (Next fix). 

## 2022-04-14

### Changed
- Removed duplicates for devices that share the same firmware file. 
- Added pop up modal when user clicks a cell of a shared firmware. 
- Cleaned code. 

### Issues
- Previously saved presets will be out of format. Please delete and create again. 
