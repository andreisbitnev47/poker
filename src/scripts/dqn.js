export default class Dqn{
    update(reward, data) {
        return new Promise((resolve, reject) => {
            fetch("/update", {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({reward, data})
            }).then((response) => {
                response.json().then(function(resp) {
                    console.log(`reward - ${reward}, data - ${data}, move - ${resp.data}`)
                    resolve(parseInt(resp.data));
                });
            })
        });
    }
}