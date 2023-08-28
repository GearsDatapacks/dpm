package gorinth

import (
	"bytes"
	"encoding/json"
	"io"
	"mime/multipart"
	"net/http"
	"os"
)

func authHeader(auth string) map[string]string {
	return map[string]string{"Authorization": auth}
}

func get(url string, headers map[string]string) (body []byte, status int) {
	client := &http.Client{}
	request, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		logError(err.Error())
	}

	for key, value := range headers {
		request.Header.Set(key, value)
	}

	response, err := client.Do(request)
	if err != nil {
		logError(err.Error())
	}

	defer response.Body.Close()
	responseBody, err := io.ReadAll(response.Body)
	if err != nil {
		logError(err.Error())
	}

	return responseBody, response.StatusCode
}

func patch(url string, payload any, headers map[string]string) (body []byte, status int) {
	requestSchema, err := json.Marshal(payload)
	if err != nil {
		logError(err.Error())
	}

	client := &http.Client{}
	request, err := http.NewRequest(http.MethodPatch, url, bytes.NewBuffer(requestSchema))
	if err != nil {
		logError(err.Error())
	}

	request.Header.Set("Content-Type", "application/json")
	for key, value := range headers {
		request.Header.Set(key, value)
	}

	response, err := client.Do(request)
	if err != nil {
		logError(err.Error())
	}

	defer response.Body.Close()
	responseBody, err := io.ReadAll(response.Body)
	if err != nil {
		logError(err.Error())
	}

	return responseBody, response.StatusCode
}

func post(url string, payload any, headers map[string]string, parts map[string]io.Reader) (body []byte, status int) {
	data, err := json.Marshal(payload)
	if err != nil {
		logError(err.Error())
	}

	requestBody := &bytes.Buffer{}
	writer := multipart.NewWriter(requestBody)

	w, err := writer.CreateFormField("data")
	if err != nil {
		logError(err.Error())
	}

	w.Write(data)

	for key, reader := range parts {
		var fileWriter io.Writer
		if x, ok := reader.(io.Closer); ok {
			defer x.Close()
		}
		if x, ok := reader.(*os.File); ok {
			fileWriter, err = writer.CreateFormFile(key, x.Name())
			if err != nil {
				logError(err.Error())
			}
		} else {
			fileWriter, err = writer.CreateFormField(key)
			if err != nil {
				logError(err.Error())
			}
		}

		if _, err = io.Copy(fileWriter, reader); err != nil {
			logError(err.Error())
		}
	}

	writer.Close()

	client := &http.Client{}
	request, err := http.NewRequest(http.MethodPost, url, requestBody)
	if err != nil {
		logError(err.Error())
	}

	request.Header.Set("Content-Type", writer.FormDataContentType())
	for key, value := range headers {
		request.Header.Set(key, value)
	}

	response, err := client.Do(request)
	if err != nil {
		logError(err.Error())
	}

	defer response.Body.Close()
	responseBody, err := io.ReadAll(response.Body)
	if err != nil {
		logError(err.Error())
	}

	return responseBody, response.StatusCode
}

func toMap[T any](object T) map[string]any {
	str, err := json.Marshal(object)

	if err != nil {
		logError(err.Error())
	}

	result := map[string]any{}

	err = json.Unmarshal(str, &result)

	if err != nil {
		logError(err.Error())
	}
	return result
}

func removeNullValues[T Project](object T) map[string]any {
	values := toMap(object)

	for key, value := range values {
		if value == nil {
			delete(values, key)
			continue
		}
	}

	return values
}

func removeZeroValues[T Project](object T) map[string]any {
	zeroStruct := T{}
	values := toMap(object)
	zeroMap := toMap(zeroStruct)

	for key, value := range values {
		if value == nil {
			delete(values, key)
			continue
		}

		if value == zeroMap[key] {
			delete(values, key)
			continue
		}
	}

	return values
}

// func Upload(client *http.Client, url string, values map[string]io.Reader) (err error) {
// 	// Prepare a form that you will submit to that URL.
// 	var b bytes.Buffer
// 	w := multipart.NewWriter(&b)
// 	for key, r := range values {
// 			var fw io.Writer
// 			if x, ok := r.(io.Closer); ok {
// 					defer x.Close()
// 			}
// 			// Add an image file
// 			if x, ok := r.(*os.File); ok {
// 					if fw, err = w.CreateFormFile(key, x.Name()); err != nil {
// 							return
// 					}
// 			} else {
// 					// Add other fields
// 					if fw, err = w.CreateFormField(key); err != nil {
// 							return
// 					}
// 			}
// 			if _, err = io.Copy(fw, r); err != nil {
// 					return err
// 			}

// 	}
// 	// Don't forget to close the multipart writer.
// 	// If you don't close it, your request will be missing the terminating boundary.
// 	w.Close()

// 	// Now that you have a form, you can submit it to your handler.
// 	req, err := http.NewRequest("POST", url, &b)
// 	if err != nil {
// 			return
// 	}
// 	// Don't forget to set the content type, this will contain the boundary.
// 	req.Header.Set("Content-Type", w.FormDataContentType())

// 	// Submit the request
// 	res, err := client.Do(req)
// 	if err != nil {
// 			return
// 	}

// 	// Check the response
// 	if res.StatusCode != http.StatusOK {
// 			err = fmt.Errorf("bad status: %s", res.Status)
// 	}
// 	return
// }
