const purgecss = require('@fullhuman/postcss-purgecss')

module.exports = {
  plugins: [
    purgecss({
      content: ['./*.html'] // Adjusted the path to match the correct location of HTML files
    })
  ]
}
