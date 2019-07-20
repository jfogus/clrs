'use strict';

const fs = require('fs');
{
    let dataPrefix = '../data/';
    let descPrefix = '../views/partials/descriptions/';
    let longDescDir = descPrefix + 'long/';
    let shortDescDir = descPrefix + 'short/';
    
    // Get races data and attach parks data based on race id
    let racesData = JSON.parse(fs.readFileSync(dataPrefix + 'races.json'));
    let parksData = JSON.parse(fs.readFileSync(dataPrefix + 'parks.json'));

    for(let i in racesData['races']) {
        for(let j in parksData['parks']) {
            if (racesData['races'][i]['park'] === parksData['parks'][j]['id']) {
                racesData['races'][i]['park'] = parksData['parks'][j]
            }            
        }
        racesData['races'][i]['description'] = {}
    }

    // Get long and short descr data and attach to racesData
    let longDescFiles = fs.readdirSync(longDescDir);
    let shortDescFiles = fs.readdirSync(shortDescDir);

    for(let i in longDescFiles) {
        let longDesc = fs.readFileSync(longDescDir + longDescFiles[i], 'utf8');
        for(let j in racesData['races']) {
            if (racesData['races'][j]['date'] === longDescFiles[i].substr(0,10).replace(/_/g, '-')) {
                racesData['races'][j]['description']['long'] = longDesc;
            }
        }
    }
    for(let i in shortDescFiles) {
        let shortDesc = fs.readFileSync(shortDescDir + shortDescFiles[i], 'utf8');
        for(let j in racesData['races']) {
            if (racesData['races'][j]['date'] === shortDescFiles[i].substr(0,10).replace(/_/g, '-')) {
                racesData['races'][j]['description']['short'] = shortDesc;
            }
        }
    }
    console.log(racesData);
}