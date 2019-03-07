This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## pre-requisites

`node-js`
`npm` or `yarn`

## 1. `node-js` installation

Using `nvm` to install `node-js` is recommended.

```sh
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash
nvm install --lts
```

## 2. `npm` or `yarn` installation

If you installed `node-js`, the `npm` would already be included in `node-js`.

If you want to use `yarn`, Visit [https://yarnpkg.com/en/docs/install#mac-stable](https://yarnpkg.com/en/docs/install#mac-stable)

or use following instruction.

### In Ubuntu Linux

execute following codes:

```sh
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
```

Install yarn by doing following code.

If you used `nvm` to install `node-js`, you can avoid the `node` installation by doing:

```sh
sudo apt-get update && sudo apt-get install --no-install-recommends yarn
```

Or, use following code to install `yarn`:

```sh
sudo apt-get update && sudo apt-get install yarn
```

After installation, check whether yarn is installed successfully.

```sh
yarn --version
```

### In MacOS

## 3. Installing application

Move to the front-end application directory (`gadgedProj/front/`) and execute following code.

In `npm`:

```sh
npm install
```

In `yarn`:

```sh
yarn
```

## 4. Running application

Move to the front-end application directory (`gadgedProj/front/`) and execute following code.

In `npm`:

```sh
npm start
```

In `yarn`:

```sh
yarn start
```

Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

You should run your back-end code in [http://localhost:8000](http://localhost:8000)

## 5. Explaination of directory

It will be updated lately.