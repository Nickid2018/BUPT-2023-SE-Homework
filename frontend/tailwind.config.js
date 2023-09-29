module.exports = {
    content: [
        './index.html',
        './src/**/*.{vue,js,ts,jsx,tsx}'
    ],
    theme: {
        extend : {
            colors: {
                primary: {
                    100: '#EDF2FB',
                    200: '#E2EAFC',
                    300: '#D7E3FC',
                    400: '#CCDBFD',
                    500: '#C1D3FE',
                    600: '#B6CCFE',
                    700: '#ABC4FF'
                }
            },
            fontFamily: {
                'sans': ['Source Han Sans SC VF', 'sans-serif']
            }
        }
    },
    plugins: []
}