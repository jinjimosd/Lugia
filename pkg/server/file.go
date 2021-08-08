/**
 * File:    file.go
 *
 * Author1:	Bui Loc Xuan Truong
 * Email:	truongblx26031999@gmail.com, truongblxhe130204@fpt.edu.vn
 * Date:   	Summmer 2021
 * Course:	CAPSTONE PROJECT (For IA Specializations)(IAP491)
 * University: 	FPT University
 *
 * Summary of File:
 *
 * 	This file contains the code related to the file handling of the EDR server.
 * 	Functions:
 * 	Read file and return all data.
 * 	Write file, add new line to file.
 */

package server

import (
	"bufio"
	"encoding/json"
	"os"
)

// The function reads all the data from the file line by line,
// converting it to a slice of map[string]interface{}
func ReadSliceMapInterface(filePath string) []map[string]interface{} {

	file, _ := os.Open(filePath)

	// create slice to add map[string]interface{}
	sliceMapInterface := make([]map[string]interface{}, 0)

	// read from file and split file to line by line
	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)

	// Add to slice each MAP after converting string to map[string]interface{}
	for scanner.Scan() {
		sliceMapInterface = append(sliceMapInterface, ConvertJsonToInterface(scanner.Text()))
	}
	defer file.Close()
	return sliceMapInterface
}

// The function reads all the data from the file line by line,
// converting it to a slice of map[string]string
func ReadSliceMapString(filePath string) []map[string]string {

	file, _ := os.Open(filePath)

	// create slice to add map[string]string
	sliceMapString := make([]map[string]string, 0)

	// read from file and split file to line by line
	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)

	// Add to slice each MAP after converting string to map[string]string
	for scanner.Scan() {
		mapInterface := ConvertJsonToInterface(scanner.Text())
		sliceMapString = append(sliceMapString, ConvertInterfaceToString(mapInterface))
	}
	defer file.Close()
	return sliceMapString
}

// The function converts all elements in the sliceMapString into bytes and stores them
// in the file line by line. Here will delete the old data and replace it with new data.
func WriteSliceMapString(filePath string, sliceMapString []map[string]string) error {

	// Delete old file
	if err := os.Remove(filePath); err != nil {
		return err
	}

	// create new file to stores data
	file, err := os.OpenFile(filePath, os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}
	writer := bufio.NewWriter(file)

	// converts all elements in the slice into bytes and stores them in
	// the file line by line
	for _, mapString := range sliceMapString {

		// encode map[string]string to json bytes
		jsonBytes, err := json.Marshal(mapString)
		if err != nil {
			return err
		}

		// store a new line json bytes to file
		if _, err = writer.Write(append(jsonBytes, 10)); err != nil {
			return err
		}
	}
	writer.Flush()
	file.Close()
	return nil
}

// The function converts all elements in the sliceMapInterface{} into bytes and stores them
// in the file line by line. Here will delete the old data and replace it with new data.
func WriteSliceMapInterface(filePath string, sliceMapInterface []map[string]interface{}) error {

	// Delete old file
	if err := os.Remove(filePath); err != nil {
		return err
	}

	// create new file to stores data
	file, err := os.OpenFile(filePath, os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}
	writer := bufio.NewWriter(file)

	// converts all elements in the slice into bytes and stores them in
	// the file line by line
	for _, mapString := range sliceMapInterface {

		// encode map[string]interface{} to json bytes
		jsonBytes, err := json.Marshal(mapString)
		if err != nil {
			return err
		}

		// store a new line json bytes to file
		if _, err = writer.Write(append(jsonBytes, 10)); err != nil {
			return err
		}
	}
	writer.Flush()
	file.Close()
	return nil
}

// The function converts a map[string]string into bytes and adds a new line to file.
func WriteMapString(filePath string, mapString map[string]string) error {

	// open file to add a new line
	file, err := os.OpenFile(filePath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}
	writer := bufio.NewWriter(file)

	// encode map[string]string to json bytes
	jsonBytes, err := json.Marshal(mapString)
	if err != nil {
		return err
	}

	// store a new line json bytes to file
	if _, err = writer.Write(append(jsonBytes, 10)); err != nil {
		return err
	}
	writer.Flush()
	file.Close()
	return nil
}

// The function converts a map[string]interface{} into bytes and adds a new line to file.
func WriteMapInterface(filePath string, mapString map[string]interface{}) error {

	// open file to add a new line
	file, err := os.OpenFile(filePath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		return err
	}
	writer := bufio.NewWriter(file)

	// encode map[string]interface{} to json bytes
	jsonBytes, err := json.Marshal(mapString)
	if err != nil {
		return err
	}

	// store a new line json bytes to file
	if _, err = writer.Write(append(jsonBytes, 10)); err != nil {
		return err
	}
	writer.Flush()
	file.Close()
	return nil
}
