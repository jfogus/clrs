'use strict';

const fs = require('fs');
const path = require('path');
const gulp = require('gulp');
const data = require('gulp-data');
const sass = require('gulp-sass');
const pug  = require('gulp-pug');
const browserSync = require('browser-sync').create();
// const tools = require('./tools/fs_utils')

sass.compiler = require('node-sass');

function reload(done) {
  browserSync.reload()
  done()
}
reload.description = 'Reload the browser'

function transPug() {
  return gulp.src([
      './views/**/*.pug',
      '!./views/partials/*',
      '!./views/templates/*'
    ])
    .pipe(data(function(file) {
      let longDescDir = './views/partials/descriptions/long/';
      let shortDescDir = './views/partials/descriptions/short/';
      
      // Get races data and attach parks data based on race id
      let racesData = JSON.parse(fs.readFileSync('./data/races.json'));
      let parksData = JSON.parse(fs.readFileSync('./data/parks.json'));

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
      
      for(let i in racesData['races']) {
        // Construct file name for images and attach to racesData
        let indexOfSuffix = racesData['races'][i]['name'].indexOf(' Run/Walk');
        if (indexOfSuffix == -1) {
          indexOfSuffix = racesData['races'][i]['name'].length;
        }
        let imgDirName = racesData['races'][i]['name'].substr(0, indexOfSuffix);
        imgDirName = imgDirName.toLowerCase().replace(/ /g, '_');
        // imgDirName = imgDirName;
        let imgFileName = imgDirName.substr(5);
        racesData['races'][i]['images'] = {
          slide: imgDirName + '/slide/' + imgFileName + '.jpg',
          still: imgDirName + '/still/' + imgFileName + '.jpg'
        };

        // Construct human readable and device readable datetime
        let date = new Date(racesData['races'][i]['date'] + 'T' + racesData['races'][i]['time']);
        racesData['races'][i]['date'] = {
          human: date.toDateString(),
          device: racesData['races'][i]['date']
        };
        racesData['races'][i]['time'] = {
          human: date.toLocaleTimeString(),
          device: racesData['races'][i]['time']
        };
      }

      // Gather results and add to racesData['results'] in the form:
      // { year: [ races ] }; { race: name, [ results ] };
      // result { name, category, time } (should be ordered from file by time ASC)
      racesData['results'] = {};
      let pastRaces = JSON.parse(fs.readFileSync('./data/past_races.json'));
      for(let i in pastRaces['races']) {
        let race = pastRaces['races'][i];
        let year = race.name.substr(0, 4);

        if (!racesData['results'][year]) {
          racesData['results'][year] = [];
        }

        let fileName = (race.date + race.name.substr(4) + '.json').replace(/-| |\//g, '_');
        let results = JSON.parse(fs.readFileSync('./data/results/' + fileName));

        racesData['results'][year].push({
          name: race.name,
          results: results['results']
        });
      }

      return racesData;
    }))
    .pipe(pug({
      doctype: 'html',
      pretty: true
    }))
    .pipe(gulp.dest('./public/'))
}
transPug.description = 'Compile pug templates into html files'

function tSass() {
  return gulp.src('./scss/**/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(gulp.dest('./public/css'))
    .pipe(browserSync.stream())
}
tSass.description = 'transpile scss to css and stream to browser'

// Start Proxy and Watch scss and html
function serve() {
  browserSync.init({
    server: {
      baseDir: './public',
      index: 'index.html'
    }
  })
}
serve.description = 'start browserSync proxy'

function watchFiles() {
  gulp.watch('./scss/**/*.scss', gulp.series(tSass))
  gulp.watch('./**/*.pug', gulp.series(transPug, reload))
}

// Start
const defaultTasks = gulp.series(gulp.parallel(tSass, transPug), gulp.parallel(watchFiles, serve))
exports.default = defaultTasks

//watch.description = 'watch scss and html for changes'

// Clean the directories
//gulp.task('clean', function() {

//});

//gulp.task('scripts', function() {

//});
