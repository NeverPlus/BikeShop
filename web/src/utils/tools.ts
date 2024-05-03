// 获取图片转base64
export function getBase64 (file: File) {
  return new Promise(function (resolve, reject) {
    const reader = new FileReader()
    let imgResult = '' as any
    reader.readAsDataURL(file)
    reader.onload = () => {
      imgResult = reader.result
    }
    reader.onerror = function (error) {
      reject(error)
    }
    reader.onloadend = function () {
      resolve(imgResult)
    }
  })
}

export function getBase64List (files: Array<any>) {
  return new Promise(function (resolve, reject) {
    const promises = files.map((file) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        let imgResult = '' as any
        reader.readAsDataURL(file.raw)
        reader.onload = () => {
          imgResult = reader.result
        }
        reader.onerror = function (error) {
          reject(error)
        }
        reader.onloadend = function () {
          resolve(imgResult)
        }
      })
    })

    Promise.all(promises)
      .then((res) => {
        resolve(res)
      })
      .catch((err) => {
        reject(err)
      })
  })
}
